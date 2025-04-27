#define _WIN32_WINNT 0x0501
#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define MAX_WATCHDOGS 256


void elevate_shutdown_privilege_once() {
    HANDLE hToken;
    TOKEN_PRIVILEGES tkp;
    if (!OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken)) return;
    if (!LookupPrivilegeValue(NULL, SE_SHUTDOWN_NAME, &tkp.Privileges[0].Luid)) return;

    tkp.PrivilegeCount = 1;
    tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    AdjustTokenPrivileges(hToken, FALSE, &tkp, 0, NULL, 0);
}


int pid_exists(DWORD pid) {
    HANDLE hProc = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
    if (hProc) {
        CloseHandle(hProc);
        return 1;
    }
    return 0;
}

void trigger_shutdown() {
    HANDLE hToken;
    TOKEN_PRIVILEGES tkp;
    OpenProcessToken(GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken);
    LookupPrivilegeValue(NULL, SE_SHUTDOWN_NAME, &tkp.Privileges[0].Luid);
    tkp.PrivilegeCount = 1;
    tkp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
    AdjustTokenPrivileges(hToken, FALSE, &tkp, 0, NULL, 0);
    ExitWindowsEx(EWX_SHUTDOWN | EWX_FORCE, 0);
}

void write_pid_list(HANDLE pipe, DWORD* pids, int count) {
    DWORD written;
    WriteFile(pipe, &count, sizeof(int), &written, NULL);
    WriteFile(pipe, pids, sizeof(DWORD) * count, &written, NULL);
}

void read_pid_list(HANDLE pipe, DWORD* out, int* out_count) {
    DWORD read;
    ReadFile(pipe, out_count, sizeof(int), &read, NULL);
    ReadFile(pipe, out, sizeof(DWORD) * (*out_count), &read, NULL);
}

void spawn_watchdogs(const char* exe_path, DWORD service_pid, int num_watchdogs) {
    if (num_watchdogs > MAX_WATCHDOGS) {
        fprintf(stderr, "Too many watchdogs\n");
        exit(1);
    }

    SECURITY_ATTRIBUTES sa = { sizeof(SECURITY_ATTRIBUTES), NULL, TRUE };
    STARTUPINFO si = { 0 };
    si.cb = sizeof(si);
    PROCESS_INFORMATION infos[MAX_WATCHDOGS];
    HANDLE write_ends[MAX_WATCHDOGS];
    DWORD pids[MAX_WATCHDOGS + 1];

    pids[0] = service_pid;

    for (int i = 0; i < num_watchdogs; i++) {
        HANDLE read_pipe, write_pipe;
        if (!CreatePipe(&read_pipe, &write_pipe, &sa, 0)) {
            fprintf(stderr, "CreatePipe failed\n");
            exit(1);
        }

        si.hStdInput = read_pipe;
        si.dwFlags = STARTF_USESTDHANDLES;

        char cmdline[256];
        snprintf(cmdline, sizeof(cmdline), "\"%s\"", exe_path);

        if (!CreateProcess(NULL, cmdline, NULL, NULL, TRUE, 0, NULL, NULL, &si, &infos[i])) {
            fprintf(stderr, "CreateProcess failed\n");
            exit(1);
        }

        CloseHandle(read_pipe);
        write_ends[i] = write_pipe;
        pids[i + 1] = infos[i].dwProcessId;
    }

    for (int i = 0; i < num_watchdogs; i++) {
        write_pid_list(write_ends[i], pids, num_watchdogs + 1);
        CloseHandle(write_ends[i]);
    }

    printf("[secure] Watchdog ring armed. PIDs:");
    for (int i = 0; i <= num_watchdogs; i++) {
        printf(" %lu", pids[i]);
    }
    printf("\n");
}

int main(int argc, char* argv[]) {
	SetPriorityClass(GetCurrentProcess(), REALTIME_PRIORITY_CLASS);
	// set priority
	
    DWORD self_pid = GetCurrentProcessId();

    if (argc == 3) {
        DWORD service_pid = atoi(argv[1]);
        int num_watchdogs = atoi(argv[2]);
        spawn_watchdogs(argv[0], service_pid, num_watchdogs);
        return 0;
    }

    if (argc == 1) {
		elevate_shutdown_privilege_once();
		
		/// TESTING BLOCK
		AllocConsole();
		freopen("CONOUT$", "w", stdout);
		freopen("CONOUT$", "w", stderr);
		printf("[WATCHDOG %lu] Attached to console.\n", GetCurrentProcessId());
		/// TESTING BLOCK
		
        DWORD pids[MAX_WATCHDOGS + 1];
		DWORD shuffled[MAX_WATCHDOGS + 1];
		int count;

		read_pid_list(GetStdHandle(STD_INPUT_HANDLE), pids, &count);
		memcpy(shuffled, pids, sizeof(DWORD) * count);

		// Optional: seed rand() per watchdog
		srand(GetCurrentProcessId());

		// Fisher-Yates shuffle
		for (int i = count - 1; i > 0; i--) {
			int j = rand() % (i + 1);
			DWORD temp = shuffled[i];
			shuffled[i] = shuffled[j];
			shuffled[j] = temp;
		}

        while (1) {
            for (int i = 0; i < count; i++) {
                if (shuffled[i] == self_pid) continue;
                if (!pid_exists(shuffled[i])) {
                    printf("[SHUTDOWN] (test placeholder)\n");
					//ExitWindowsEx(EWX_SHUTDOWN | EWX_FORCE, 0);
                    return 0;
                }
            }
			
			Sleep(1 + (rand() % 3));
        }
    }

    fprintf(stderr, "Usage:\n  %s <service_pid> <num_watchdogs>\n", argv[0]);
    return 1;
}
