#include <emscripten.h>
#include <math.h>
#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

char tabID[200];
int isAllowed();

char* sanitize_value() {
    if (isAllowed()) {
        return tabID;
    }

    return "tab-it";
}

int isAllowed() {
    char whitelist[2][10] = {"tab-wr", "tab-it"};
    char buffer[190] = {0};
    char *tmp = tabID;

    memcpy(buffer, tmp, strlen(tmp));
    buffer[189] = '\0';

    for (int i = 0; i < 2; i++) {
        if (strstr(buffer, whitelist[i]) != NULL) {
            return 1;
        }
    }

    return 0;
}
