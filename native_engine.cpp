
#include <iostream>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>

extern "C" {
    int fast_scan_port(const char* ip, int port) {
        int sock = socket(AF_INET, SOCK_STREAM, 0);
        if (sock == -1) return -1;

        sockaddr_in hint;
        hint.sin_family = AF_INET;
        hint.sin_port = htons(port);
        inet_pton(AF_INET, ip, &hint.sin_addr);

        struct timeval tv;
        tv.tv_sec = 0;
        tv.tv_usec = 200000; // 200ms timeout for ultra scan
        setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof tv);

        int result = connect(sock, (sockaddr*)&hint, sizeof(hint));
        close(sock);
        
        if (result == 0) return 1; // Open
        return 0; // Closed
    }
}
