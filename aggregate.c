#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 128
#define MAX_COMMAND_LENGTH 512

int main() {
    char line[MAX_LINE_LENGTH];
    int htrLength = 0;

    FILE *inputFile = fopen("output.txt", "r");
    FILE *returnFile = fopen("return.txt", "w");
    FILE *lengthFile = fopen("length.txt", "w");
    FILE *outHtrFile = fopen("outhtr.txt", "w");
    FILE *countFile = fopen("count.txt", "w");
    fclose(returnFile);
    fclose(lengthFile);
    fclose(outHtrFile);
    fclose(countFile);

    returnFile = fopen("return.txt", "r");
    outHtrFile = fopen("outhtr.txt", "a");
    lengthFile = fopen("length.txt", "a");
    countFile = fopen("count.txt", "a");

    while (fgets(line, MAX_LINE_LENGTH, inputFile) != NULL) {
        char command[MAX_COMMAND_LENGTH];
        snprintf(command, MAX_COMMAND_LENGTH, "nissy solve htr \"%s\" | tee -a return.txt", line);
        system(command);
    }

    while (fgets(line, MAX_LINE_LENGTH, returnFile)) {
        char *open_paren = strchr(line, '(');
        char *close_paren = strchr(line, ')');
        if (open_paren != NULL && close_paren != NULL) {
            char number_str[5];
            int num_length = close_paren - open_paren - 1;

            if (num_length > 0 && num_length < sizeof(number_str)) {
                strncpy(number_str, open_paren + 1, num_length);
                number_str[num_length] = '\0';
                htrLength = atoi(number_str);
                fprintf(lengthFile, "%s\n", number_str);
                fflush(stdout);
            }
        }
    }
    fclose(lengthFile);
    fseek(inputFile, 0, SEEK_SET);
    lengthFile = fopen("length.txt", "r");
    fseek(lengthFile, 0, SEEK_SET);

    while (fgets(line, MAX_LINE_LENGTH, inputFile) != NULL) {
        fflush(stdin);
        fscanf(lengthFile, "%d\n", &htrLength);
        char command[MAX_COMMAND_LENGTH];
        snprintf(command, MAX_COMMAND_LENGTH, "nissy solve htr -c -M %d \"%s\" | tee -a count.txt", htrLength, line);
        system(command);
    }
    return 0;
}
