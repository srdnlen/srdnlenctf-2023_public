#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <stdbool.h>
#include <string.h>



char video_ascii[3000];


void clearScreen(){
    system("clear");
}

void printVideo(){
    clearScreen();
    printf("%s", video_ascii);
    
}

void cleanBuffer(){
    while(getchar() != '\n');
}

void printLogo(){
    printf("┌───┐\n"
    "│ ► │PwnTube\n"
    "└───┘\n");
    
}

void togglePlayStop(bool isPlaying){
    char* video_ascii_stop = "┌───┐\n"
    "│ ► │PwnTube\n"
    "└───┘\n"
    "\n"
    "┌─────────────────────────────────────────────────────────┐\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠿⠟⠛⠻⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣆⣀⣀⠀⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠻⣿⣿⣿⠅⠛⠋⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢼⣿⣿⣿⣃⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣟⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣛⣛⣫⡄⠀⢸⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⢀⣠⣴⣾⡆⠸⣿⣿⣿⡷⠂⠨⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⣤⣾⣿⣿⣿⣿⡇⢀⣿⡿⠋⠁⢀⡶⠪⣉⢸⣿⣿⣿⣿⣿⣇⠀⠀               │\n"
    "│              ⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⡏⢸⣿⣷⣿⣿⣷⣦⡙⣿⣿⣿⣿⣿⡏⠀⠀               │\n"
    "│              ⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣿⣿⣿⣿⣿⣷⣦⣿⣿⣿⣿⣿⡇⠀⠀               │\n"
    "│              ⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀               │\n"
    "│              ⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀               │\n"
    "│              ⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀               │\n"
    "│              ⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀               │\n"
    "│              ⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀  Skip ad ►│   │\n"
    "│ ►   ►|       ⠀⠀⢹⣿⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡁⠀⠀               │\n"
    "└─────────────────────────────────────────────────────────┘\n"
    " [Tutorial] How to get the flag\n"
    "\n"
    "                                   2 likes, 69 dislikes\n";

    char* video_ascii_playing = "┌───┐\n"
    "│ ► │PwnTube\n"
    "└───┘\n"
    "\n"
    "┌─────────────────────────────────────────────────────────┐\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣶⣿⣿⣿⣿⣿⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣿⣿⠿⠟⠛⠻⣿⠆⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣆⣀⣀⠀⣿⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠻⣿⣿⣿⠅⠛⠋⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢼⣿⣿⣿⣃⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣟⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣛⣛⣫⡄⠀⢸⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⠀⠀⢀⣠⣴⣾⡆⠸⣿⣿⣿⡷⠂⠨⣿⣿⣿⣿⣶⣦⣤⣀⠀⠀⠀               │\n"
    "│              ⠀⠀⠀⣤⣾⣿⣿⣿⣿⡇⢀⣿⡿⠋⠁⢀⡶⠪⣉⢸⣿⣿⣿⣿⣿⣇⠀⠀               │\n"
    "│              ⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⡏⢸⣿⣷⣿⣿⣷⣦⡙⣿⣿⣿⣿⣿⡏⠀⠀               │\n"
    "│              ⠀⠀⠈⣿⣿⣿⣿⣿⣿⣿⣿⣇⢸⣿⣿⣿⣿⣿⣷⣦⣿⣿⣿⣿⣿⡇⠀⠀               │\n"
    "│              ⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀               │\n"
    "│              ⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠀               │\n"
    "│              ⠀⠀⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀               │\n"
    "│              ⠀⠀⣠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠀               │\n"
    "│              ⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀  Skip ad ►│   │\n"
    "│ ||  ►|       ⠀⠀⢹⣿⣵⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⡁⠀⠀               │\n"
    "└─────────────────────────────────────────────────────────┘\n"
    " [Tutorial] How to get the flag\n"
    "\n"
    "                                   2 likes, 69 dislikes\n";


    if (!isPlaying){
        strcpy(video_ascii, video_ascii_stop);
    }
    else{
        strcpy(video_ascii, video_ascii_playing);
    }
}

void skipAd(int x, int y){
    clearScreen();
    char cmd[15] = "cat ./flag.txt";
    if (x == 0xdeadbeef && y == 0xfeedface){
        printf("\nYou did not give me up :)\nYou earned this:\n\n");

        system(cmd);
        
    }
    else{
        system("cat ./flag");
    }
}

int menu(){
    int choice;
    
    printf("\n 1. Play/Stop\t2. Skip ad\t3. Show comments     4. Add comment\t5. Buy Premium\t 0. Quit\n");
    printf("─────────────────────────────────────────────────────────────────────────────────────────────────\n");
    
    scanf("%d", &choice);
    cleanBuffer();
    
    return choice;
}

void showComments(char comments[][30], int n_comments){
    clearScreen();
    printLogo();
    printf("\n\nComments\n"
           "─────────\n");
    
    for (int i=0; i < n_comments; i++){
        printf(comments[i]);
    }
    

}
void addComment(char comments[][30], int* n_comments){
    clearScreen();
    printLogo();
    if (*n_comments < 10){
        printf("Enter your comment here:\n");
        
        scanf("%7s", comments[*n_comments]);
        cleanBuffer();

        if (strstr(comments[*n_comments], "%p") != NULL || strstr(comments[*n_comments], "%x") != NULL){
            printf("Plz don't hack me :(\n");
            
            strcpy(comments[*n_comments], "never gonna hack me");
        }

        strcat(comments[*n_comments], "\n");
        *n_comments += 1;
    }
    else{
        printf("Too many comments!");
        
    }
    

}

void to_be_implemented_yet(){
    asm("pop %rdi; pop %rdi; pop %rsi; pop %rdi; ret");
}

void buy_premium(){
    int choice;
    char name[500];
    char card_number[17];
    float balance = 0.0;

    clearScreen();
    printf("Enjoy watching PwnTube uninterrupted by ads.\n"
    "Get as many flags as you want, on your mobile device, desktop, or smart TV.\n"
    "\tAll of this, just for €19.99/month\n");

    printf("\nCurrent balance: €%.2f.\n", balance);

    printf("1. Buy Premium now\t2. Add funds\t3. Go back\n");
    
    scanf("%d", &choice);
    cleanBuffer();

    switch(choice){
        case 1:
            if (balance >=  19){
                skipAd(0xdeadbeef, 0xfeedface);
            }
            else{
                printf("You don't have enough money\n");
                
            }
                
            return;
        case 2:
            printf("Insert your name:\n");
            
            scanf("%s", name);
            cleanBuffer();
            
            printf("Insert your card number:\n");
            
            scanf("%16s", card_number);
            cleanBuffer();

            printf("Processing payment...\n");
            
            sleep(5);
            
            printf("Payment failed, you're broke\n");

            break;
        case 3:
            printVideo();
            return;
    }
    return;
}

int main(){
    int choice;
    bool isPlaying = true;
    char comments[10][30] = {
        "Nice video!\n",
        "This chall was too easy lol\n",
        "ggwp\n",
        "Find a real job bro\n",
        "Too many ads\n",
        "Guys can u send me the flag\n",
        "flag: srdnlen{rick_astley}\n",
        "First!!! :D\n"
    };
    int n_comments = 8;
    bool debug=false;
    bool premium=false;

    setvbuf(stdout, NULL, _IONBF, 0);

    togglePlayStop(isPlaying);

    printVideo(); 
    
    while(1){
        
        choice = menu();

        switch(choice){
            case 0:
                printf("See you :)\n");
                return 0;
            case 1:
                isPlaying = !isPlaying;
                togglePlayStop(isPlaying);
                printVideo();
                break;
            case 2:
                printf("Buy PwnTube Premium to have an ad-free experience <3\n");
                break;
            case 3:
                showComments(comments, n_comments);
                break;
            case 4:
                addComment(comments, &n_comments);
                break;
            case 5:
                if(debug){
                    buy_premium();
                }
                else{
                    printf("Sorry, this functionality is under maintenance :)");
                }
                
                break;
            case 777:
                debug = !debug;
                break;
            case 0xb05a:
                printf("Wow you finally found the flag!\nJust wait a sec i'll get it for you\n");
                
                sleep(30);

                system("cat ./flag");
                break;
            default:
                printVideo();
                break;
        }
    }
    return 0;
}



