#include <stdlib.h>
#include <stdio.h>
#include <string.h>

// Compile with PIE so that we can run the win function in the base instead of a gadget in the libc with more or less the same difficulty (instead of being trivial without PIE)
// gcc -no-pie --static -o gep main.c

#define BOARD_W 8
#define BOARD_H 8

#define UNIQUE_PIECES 7

const char* player_names[] = {"White", "Black"};


const char* wiki_pos = "r1bq1rk1/pp3ppp/3n4/2p1N3/2B5/7P/PPP2PP1/R1BQR1K1 w";
const char* starting_pos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1";
//const char* test_crash = "8888888r/8888888r/8888888r/8888888r/8888888r/8888888r/8888888r/8888888r w KQkq - 0 1";



enum castle_direction {
    WHITE_KS,
    WHITE_QS,
    BLACK_KS,
    BLACK_QS
};

enum to_move {
    WHITE,
    BLACK
};

enum piece_type {
    KING,
    QUEEN,
    ROOK,
    BISHOP,
    KNIGHT,
    PAWN, 
    EMPTY
};

struct chessboard {
    char pieces[BOARD_H*BOARD_W];
    enum to_move current_move;
    int can_castle[4];
    int fifty_moves_ctr; // Technically counts 100 half moves.
    int move_ctr; // Incremented after every black turn. 
};

const char default_pieces[UNIQUE_PIECES*2 + 2] = {
    'K',
    'Q',
    'R',
    'B',
    'N',
    'P',
    ' ',
    'k',
    'q',
    'r',
    'b',
    'n',
    'p',
    ' ',  
     // Custom piece indicating en passantable square. Default is asterisk.
    '*',
    '\0'    
};

void printBoard(struct chessboard* cb) {
    for(int i = 0; i < BOARD_H*BOARD_W; i++){
        printf("| %c ", cb->pieces[i]);
        if (i%8 == 7) printf("| \n---------------------------------\n");
    }
    printf("Move no. %d, %s to move. \n flags: castles: %d %d %d %d, half-move draw count: %d\n\n", 
    cb->move_ctr, player_names[cb->current_move], cb->can_castle[0], cb->can_castle[1], cb->can_castle[2], cb->can_castle[3], cb->fifty_moves_ctr);
}

/* void win() {
    if(!getenv("FLAG")) {
        printf("Error reading flag env. If you see this in the CTF, call an admin.");
        exit(1);
    } else{
        printf("%s", getenv("FLAG"));
    }
} */

void createEmptyBoard(struct chessboard* board) {
    for(int i = 0; i < BOARD_H*BOARD_W; i++){
        board->pieces[i] = default_pieces[6]; //Init to white-normal-empty.
    }
    for(int i = 0; i < 4; i++){
        board->can_castle[i] = 0;
    }
    board->current_move = WHITE;
    board->fifty_moves_ctr = 0;
    board->move_ctr = 0;
}

void createDefaultPieces(char* pieces) {
    for(int i = 0; i < 2*UNIQUE_PIECES + 2; i++){
        pieces[i] = default_pieces[i]; //Init to default pieces.
    }
}

void readFEN(const char* position, char* chess_set, struct chessboard* board){
    int str_read_idx = 0;
    int max_idx = strlen(position);
    // Starting position read
    char c;
    int cur_row = 0;
    int cur_col = 0;

    printf("Reading position [%s] ... \n", position);


    while ( (str_read_idx < max_idx) &&  (cur_row < BOARD_H) && (' ' != (c = position[str_read_idx++]) ) ){
        if (c > '0' && c < '9'){
            int skip = (c-'0');
            cur_col += skip;
            //printf("Skipped %d slots, current col: %d\n", skip, cur_col);
        }
        else if (c == '/') {
            //printf("end row\n");
            cur_row += 1;
            cur_col = 0;
        }
        else if (strchr(default_pieces, c) != NULL) {
            int chess_piece = strchr(default_pieces, c) - default_pieces;
            int piece_pos = cur_row*BOARD_W + cur_col;
            //printf("Writing piece %c in slot %d\n", chess_set[chess_piece], piece_pos);
            board->pieces[piece_pos] = chess_set[chess_piece];
            cur_col += 1;
        }
        else {
            printf("Unrecognized character in FEN string (position): %c\n Exiting...", c);
            exit(1);
        }
    }

    if (str_read_idx < max_idx) return;

    // To move read
    while ((str_read_idx < max_idx) && (' ' != (c = position[str_read_idx++]))){
        switch (c) {
            case 'w':
                board->current_move = WHITE;
                break;
            case 'b':
                board->current_move = BLACK;
                break;
            default:
                printf("Unrecognized character in FEN string (to_move): %c\n Exiting...", c);
                exit(1);
        }            
    }

    if (str_read_idx < max_idx) return;

    // Castle read:
    while ((str_read_idx < max_idx) && (' ' != (c = position[str_read_idx++]))){
        switch (c) {
            case 'K':
                board->can_castle[0] = 1;
                break;
            case 'Q':
                board->can_castle[1] = 1;
                break;
            case 'k':
                board->can_castle[2] = 1;
                break;
            case 'q':
                board->can_castle[3] = 1;
                break;
            case '-': // No need to do anything. Just keep reading
                break;
            default:
                printf("Unrecognized character in FEN string (can_castle): %c\n Exiting...", c);
                exit(1);
        }            
    }

    if (str_read_idx < max_idx) return;

    // en passant read
    int ep_slot = 0;

    while ((str_read_idx < max_idx) && (' ' != (c = position[str_read_idx++]))){
        switch (c) {
            case '-': // No need to do anything. Just keep reading
                ep_slot = -1;
                break;
            case 'a':
            case 'b':
            case 'c':
            case 'd':
            case 'e':
            case 'f':
            case 'g':
            case 'h':
                ep_slot += (c - 'a');
                break;
            case '3':
                ep_slot += 40; // Our chessboard is oriented from the top left A8 square.
                break;
            case '6':
                ep_slot += 16; // Our chessboard is oriented from the top left A8 square.
                break;
            default:
                printf("Unrecognized character in FEN string (en_passant): %c\n Exiting...", c);
                exit(1);
        }            
    }
    printf("marking piece at slot %d for en passant\n", ep_slot);
    if (ep_slot >=0) board->pieces[ep_slot] = chess_set[UNIQUE_PIECES*2];

    if (str_read_idx < max_idx) return;

    // Halfmove read 
    while ((str_read_idx < max_idx) && (' ' != (c = position[str_read_idx++]))){
        switch (c) {
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                board->fifty_moves_ctr *= 10;
                board->fifty_moves_ctr += (c - '0');
                break;
            default:
                printf("Unrecognized character in FEN string (fifty_moves): %c\n Exiting...", c);
                exit(1);
        }            
    }

    if (str_read_idx < max_idx) return;

    // Move num read
        while ((str_read_idx < max_idx) && (' ' != (c = position[str_read_idx++]))){
        switch (c) {
            case '0':
            case '1':
            case '2':
            case '3':
            case '4':
            case '5':
            case '6':
            case '7':
            case '8':
            case '9':
                board->move_ctr *= 10;
                board->move_ctr += (c - '0');
                break;
            default:
                printf("Unrecognized character in FEN string (move_num): %c\n Exiting...", c);
                exit(1);
        }            
    }

}

void customizeChessSet(char* pieces){

    struct chessboard b;
    createEmptyBoard(&b);
    char c;

    printf("Send me 15 characters and I'll set them up.\n");
    for (int i = 0; i < 15; i++){
        c = getchar();
        pieces[i] = c;
        if (c == 0 || c == '\n') break;
    };
    printf("Your custom chess set looks like this:\n");

    readFEN(starting_pos, pieces, &b);
    printBoard(&b);
}


int main()
{    
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);


    char input_buf[100];
    struct chessboard board;
    char pieces[2*UNIQUE_PIECES+2];
    int c;    

    createDefaultPieces(pieces);
    createEmptyBoard(&board);

    for(;;) {
        puts("1) Visualize FEN position \n2) Customize your chess set \n3) Quit.\n\n");
        scanf("%d", &c);
        getchar();
        if (c == 1) {
            createEmptyBoard(&board);
            printf("Give me your position in FEN format (no brackets): ");
            fgets(input_buf, 99, stdin);
            input_buf[strcspn(input_buf, "\r\n")] = 0;         
            readFEN(input_buf, pieces, &board);
            printBoard(&board);
        }
        else if (c == 2) {
            createDefaultPieces(pieces);
            customizeChessSet(pieces);
        }
        else if (c == 3) return 0;
        else printf("Sorry, try again.\n");
    }

    return 0;
}