#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <stdlib.h>
#include <string.h>

int main(){
    int htrLength = 0;
    char command[512] = "";
    char line[128] = "";
    char line3[128] = "";
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
    while (fgets(line, sizeof(line), inputFile) != NULL) {
    snprintf(command, sizeof(command), "nissy solve htr \"%s\" | tee -a return.txt", line);
    system(command);
    }
    while (fgets(line3, sizeof(line3), returnFile)) {
    char *open_paren = strchr(line3, '(');
    char *close_paren = strchr(line3, ')');
    if (open_paren != NULL && close_paren != NULL) {
            char number_str[4];
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
    while (fgets(line, sizeof(line), inputFile) != NULL) {
            fflush(stdin);
            fscanf(lengthFile, "%d\n", &htrLength);
            snprintf(command, sizeof(command), "nissy solve htr -c -M %d \"%s\" | tee -a count.txt", htrLength, line);
            system(command);
    }
    return 0;
}



