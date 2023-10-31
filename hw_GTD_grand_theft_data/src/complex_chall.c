#include <stdio.h>
#include <string.h>

int complex_operation(unsigned int res, int count) { 
	unsigned int z; 
 	
    		
	z = res;
	switch (count){
		case 0:
			//0x4b5b76fa
			z *= 2;
			z -= (0x4b5b76fa * 2) - 1;
			return z;
		case 1:
			//0xddd71e0
			z *= 2;
			z -= (0xddd71e0 * 2) - 1;
			return z;
		case 2:
			//0x1738d612
			z *= 2;
			z -= (0x1738d612 * 2) - 1;
			return z;
		case 3:
			//0x14ef173
			z *= 2;
			z -= (0x14ef173 * 2) - 1;
			return z;
		case 4:
			//0xd6d69107
			z *= 2;
			z -= (0xd6d69107 * 2) - 1;
			return z;
		case 5:
			//0x2a34198e
			z *= 2;
			z -= (0x2a34198e * 2) - 1;
			return z;
		case 6:
			//0x82f820af
			z *= 2;
			z -= (0x82f820af * 2) - 1;
			return z;
		case 7:
			//0xbef47208
			z *= 2;
			z -= (0xbef47208 * 2) - 1;
			return z;
		case 8:
			//0x95503314
			z *= 2;
			z -= (0x95503314 * 2) - 1;
			return z;
		case 9:
			//0x8c6cf6ef
			z *= 2;
			z -= (0x8c6cf6ef * 2) - 1;
			return z;
		case 10:
			//0xd804fa15
			z *= 2;
			z -= (0xd804fa15 * 2) - 1;
			return z;
		case 11:
			//0x10bfe6b
			z *= 2;
			z -= (0x10bfe6b * 2) - 1;
			return z;
		case 12:
			//0xe677cc7b
			z *= 2;
			z -= (0xe677cc7b * 2) - 1;
			return z;
		case 13:
			//0x9ef6a05a
			z *= 2;
			z -= (0x9ef6a05a * 2) - 1;
			return z;
		case 14:
			//0x7cbd93e4
			z *= 2;
			z -= (0x7cbd93e4 * 2) - 1;
			return z;
		case 15:
			//0x1bec7d04
			z *= 2;
			z -= (0x1bec7d04 * 2) - 1;
			return z;
		case 16:
			//0xd9929855
			z *= 2;
			z -= (0xd9929855 * 2) - 1;
			return z;
		case 17:
			//0x9f7e8df4
			z *= 2;
			z -= (0x9f7e8df4 * 2) - 1;
			return z;
		case 18:
			//0x5c2d05b7
			z *= 2;
			z -= (0x5c2d05b7 * 2) - 1;
			return z;
		case 19:
			//0x5d5cb1cb
			z *= 2;
			z -= (0x5d5cb1cb * 2) - 1;
			return z;
		case 20:
			//0xf8691687
			z *= 2;
			z -= (0xf8691687 * 2) - 1;
			return z;
		case 21:
			//0x72d63aae
			z *= 2;
			z -= (0x72d63aae * 2) - 1;
			return z;
		case 22:
			//0xdb777ec7
			z *= 2;
			z -= (0xdb777ec7 * 2) - 1;
			return z;
		case 23:
			//0xb065705a
			z *= 2;
			z -= (0xb065705a * 2) - 1;
			return z;
		case 24:
			//0x7cbd93e4
			z *= 2;
			z -= (0x7cbd93e4 * 2) - 1;
			return z;
		case 25:
			//0x7a42c091
			z *= 2;
			z -= (0x7a42c091 * 2) - 1;
			return z;
		case 26:
			//0x93a5a564
			z *= 2;
			z -= (0x93a5a564 * 2) - 1;
			return z;
	}
       	//printf("%d", z);	
    return z;  
 
 	//printf("%d", max);
    	 
 	//printf("%d", z);
    	
		
}

int check(char* license){
	unsigned int result[27]; 
	int count = 0, b;
	int var1, var2;
  	int var3, var4, var5, var6, var7, var8, var9, var10, var11, var12, var13, var14, var15, var16, var17, var18, var19, var20, var21, var22, var23, var24, var25, var26, var27, var28, var29, var30, var31, var32;
	//unsigned int enc[] = {, , , , , , , , , , , , , , , }; 
	for (int i = 1; i<28; i++){
    		var1 = license[i - 1];
    		var2 = license[i];
    
    		var3 = var1 * 2 + var2 - 5;
    		var4 = var2 / var1 + 3;
    		var5 = var3 + var4 * 2 - 7;
    		var6 = var5 % var1 + 4;
    		var7 = var3 * var2 - var4 / 2 + 6;
    		var8 = var7 - var2 + 8;
    		var9 = var4 * 3 + var6 / 2 + 9;
    		var10 = var5 + var8 - var9 * 4;
    		var11 = var1 * 2 + var4 * 3 + 7;
    		var12 = var7 / 2 + var10 * 2 - 6;
    		var13 = var6 * 4 + var9 + 5;
    		var14 = var2 * 3 + var3 / 2 - 4;
    		var15 = var14 * 2 + var13 - var7 / 3;
    		var16 = var11 - var9 * 2 + var5 / 4;
    		var17 = var15 + var12 * 3 - var8 / 2;
    		var18 = var16 / 4 + var14 - var10 * 2;
    		var19 = var17 + var18 * 2 - var11 / 3;
    		var20 = var12 * 4 - var19 + 6; 
    		var21 = var20 + var19 - var18 * 2 + var17 / 3;
    		var22 = var11 * 4 - var16 + var15 / 2 - var14 * 3;
    		var23 = var10 + var9 * 2 - var8 / 4 + var7;
    		var24 = var13 / 3 - var12 * 2 + var11 + var10 * 4;
    		var25 = var9 - var8 * 2 + var7 + var6 / 4;
    		var26 = var12 * 3 - var11 / 2 + var10 + var9 * 4;
    		var27 = var7 + var6 * 2 - var5 + var4 / 3;
    		var28 = var5 / 4 - var4 * 2 + var3 + var2 * 3;
    		var29 = var3 * 3 - var2 + var1 / 4 - var20;
    		var30 = var4 - var3 * 2 + var2 + var1 / 3;
    		var31 = var21 * var22 - var23 + var24 * var25 + var26 - var27 / var28; 
    		var32 = var29 - var30 * var31 + var22 / var23 - var24 * var25; 
  		    
    		result[i-1] = var32 * var27 + var30 - var24 + var25 * var21 - var27 / var28 + var29 % var10 + var11 * var12 - var13 / var14; 
		//printf("%x", result[i - 1]);
		license[i] = result[i-1];
		//printf("%d\n", result[i - 1] == enc[i - 1]);		
		//printf("%x\n", enc[i - 1]); 
		
		//if (result[i - 1] == enc[i - 1])
		//	count += 1;
		
		//b = result[i - 1] == enc[i - 1];
		//printf(b);
		count += complex_operation(result[i - 1], count);
		//printf("%d", count);		
	}
	

	if (count == 27){
		return 1;
	}

	return 0;
}

int main(int argc, char *argv[]){
	

	if (argc != 2){
		fprintf(stderr, "Usage ./chall flag\n");
		return 0;
	}

	char *license = argv[1];
	//printf("Insert your License: ");
	if (strlen(license) != 28){
		fprintf(stderr, "your flag must be 28 characters long\n");
		return 0;
	}
	//complex_operation(1);
	
	int a;
	a = check(license);

	if(a){
		printf("Go submit your flag!\n");
	}else{
		printf("Nope :(\n");
	}

	return 0;

}
