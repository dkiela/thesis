
/* A Bison parser, made by GNU Bison 2.4.1.  */

/* Skeleton implementation for Bison's Yacc-like parsers in C
   
      Copyright (C) 1984, 1989, 1990, 2000, 2001, 2002, 2003, 2004, 2005, 2006
   Free Software Foundation, Inc.
   
   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.
   
   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* C LALR(1) parser skeleton written by Richard Stallman, by
   simplifying the original so-called "semantic" parser.  */

/* All symbols defined below should begin with yy or YY, to avoid
   infringing on user name space.  This should be done even for local
   variables, as they might otherwise be expanded by user macros.
   There are some unavoidable exceptions within include files to
   define necessary library symbols; they are noted "INFRINGES ON
   USER NAME SPACE" below.  */

/* Identify Bison output.  */
#define YYBISON 1

/* Bison version.  */
#define YYBISON_VERSION "2.4.1"

/* Skeleton name.  */
#define YYSKELETON_NAME "yacc.c"

/* Pure parsers.  */
#define YYPURE 0

/* Push parsers.  */
#define YYPUSH 0

/* Pull parsers.  */
#define YYPULL 1

/* Using locations.  */
#define YYLSP_NEEDED 0



/* Copy the first part of user declarations.  */

/* Line 189 of yacc.c  */
#line 3 "parse.y"

#include <string.h>
#include <math.h>
#include <sys/stat.h>

#include "input.h"
#include "proto.h"
#include "FileStack.h"
#include "../defines.h"

#define TRUE  1
#define FALSE 0
#define VSIZE 100

extern TMP_INPUT *TIN;       /* This must be global so parse.y can access it */

T_BRAIN           *brain;           /* These are temporary pointers, to whatever */
T_CSHELL          *csh;             /* element the parser is working on          */
T_COLUMN          *column;
T_LSHELL          *lsh;
T_LAYER           *layer;
T_CELL            *cell;
T_CMP             *cmp;
T_CHANNEL         *chan;
T_SYNAPSE         *syn;
T_SYN_FD          *syn_fd;
T_SYNLEARN        *syn_learn;
T_SYNDATA         *syn_data;
T_SYNPSG          *syn_psg;
T_SYNAUGMENTATION *syn_augmentation;
T_SPIKE           *spike;
T_STIMULUS        *stim;
T_STINJECT        *sti;
T_REPORT          *report;
T_EVENT           *event;

FileStack fileStack;       /* incase there are multiple files being parsed */
int initFlag = 0;          /* flag to indicate if the file stack is ever used */
extern char* currentFile;  /* name of file currently being parsed */

int i, nval;               /* For reading a list of numbers of unknown length */
double vlist [VSIZE];
double *twoptr;
double *allocVlist (int, double *);
double *allocRVlist (int, double *);


/* Line 189 of yacc.c  */
#line 121 "parse.c"

/* Enabling traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif

/* Enabling verbose error messages.  */
#ifdef YYERROR_VERBOSE
# undef YYERROR_VERBOSE
# define YYERROR_VERBOSE 1
#else
# define YYERROR_VERBOSE 0
#endif

/* Enabling the token table.  */
#ifndef YYTOKEN_TABLE
# define YYTOKEN_TABLE 0
#endif


/* Tokens.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
   /* Put the tokens into the symbol table, so that GDB and other debuggers
      know about them.  */
   enum yytokentype {
     REAL = 258,
     INTEGER = 259,
     LOGICAL = 260,
     NAME = 261,
     TK_ABSOLUTE_USE = 262,
     TK_AMP_END = 263,
     TK_AMP_START = 264,
     TK_ASCII = 265,
     TK_BRAIN = 266,
     TK_CA_EXP = 267,
     TK_CA_EXTERNAL = 268,
     TK_CA_HALF_MIN = 269,
     TK_CA_INTERNAL = 270,
     TK_CA_SCALE = 271,
     TK_CA_SPIKE_INC = 272,
     TK_CA_TAU = 273,
     TK_CA_TAU_SCALE = 274,
     TK_CELL = 275,
     TK_CELLS = 276,
     TK_CELLS_PER_FREQ = 277,
     TK_CELL_TYPE = 278,
     TK_CHANNEL = 279,
     TK_COLUMN = 280,
     TK_CSHELL = 281,
     TK_COLUMN_TYPE = 282,
     TK_CMP = 283,
     TK_G = 284,
     TK_CONNECT = 285,
     TK_DATA_LABEL = 286,
     TK_DELAY = 287,
     TK_DEPR_TAU = 288,
     TK_DURATION = 289,
     TK_DYN_RANGE = 290,
     TK_END_BRAIN = 291,
     TK_END_COLUMN = 292,
     TK_END_CSHELL = 293,
     TK_END_CMP = 294,
     TK_END_CELL = 295,
     TK_END_CHANNEL = 296,
     TK_END_LAYER = 297,
     TK_END_LSHELL = 298,
     TK_END_REPORT = 299,
     TK_END_SPIKE = 300,
     TK_END_STIMULUS = 301,
     TK_END_ST_INJECT = 302,
     TK_END_SYNAPSE = 303,
     TK_END_SYN_DATA = 304,
     TK_END_SYN_FD = 305,
     TK_END_SYN_PSG = 306,
     TK_END_SYN_LEARN = 307,
     TK_E_HALF_MIN_H = 308,
     TK_E_HALF_MIN_M = 309,
     TK_FACIL_TAU = 310,
     TK_FILENAME = 311,
     TK_FREQUENCY = 312,
     TK_FREQ_ROWS = 313,
     TK_FREQ_START = 314,
     TK_FSV = 315,
     TK_HEIGHT = 316,
     TK_H_INITIAL = 317,
     TK_H_POWER = 318,
     TK_IGNORE_EMPTY = 319,
     TK_INJECT = 320,
     TK_INTERACTIVE = 321,
     TK_LAYER = 322,
     TK_LSHELL = 323,
     TK_LAYER_TYPE = 324,
     TK_LEAK_G = 325,
     TK_LEAK_REVERSAL = 326,
     TK_LEARN = 327,
     TK_LEARN_LABEL = 328,
     TK_LOCATION = 329,
     TK_LOWER = 330,
     TK_MAX_G = 331,
     TK_MODE = 332,
     TK_M_INITIAL = 333,
     TK_M_POWER = 334,
     TK_NEG_HEB_WINDOW = 335,
     TK_PATTERN = 336,
     TK_POS_HEB_WINDOW = 337,
     TK_PROB = 338,
     TK_PSG_FILE = 339,
     TK_RELOAD_SYN = 340,
     TK_REPORT = 341,
     TK_REPORT_ON = 342,
     TK_REVERSAL = 343,
     TK_RSE = 344,
     TK_RSE_LABEL = 345,
     TK_R_MEMBRANE = 346,
     TK_SAMESEED = 347,
     TK_SAVE_SYN = 348,
     TK_SEED = 349,
     TK_SFD = 350,
     TK_SFD_LABEL = 351,
     TK_SLOPE_H = 352,
     TK_SLOPE_M = 353,
     TK_SPIKE = 354,
     TK_STIMULUS = 355,
     TK_SPIKE_HW = 356,
     TK_ST_INJECT = 357,
     TK_STIM_TYPE = 358,
     TK_SYNAPSE = 359,
     TK_STRENGTH = 360,
     TK_SYN_DATA = 361,
     TK_SYN_FD = 362,
     TK_SYN_LEARN = 363,
     TK_SYN_PSG = 364,
     TK_SYN_REVERSAL = 365,
     TK_TAU_MEMBRANE = 366,
     TK_TAU_SCALE_M = 367,
     TK_TAU_SCALE_H = 368,
     TK_THRESHOLD = 369,
     TK_TIME_END = 370,
     TK_TIME_START = 371,
     TK_TIME_FREQ_INC = 372,
     TK_TIMING = 373,
     TK_TYPE = 374,
     TK_UPPER = 375,
     TK_UNITARY_G = 376,
     TK_VMREST = 377,
     TK_VOLTAGES = 378,
     TK_VTAU_VAL_M = 379,
     TK_VTAU_VAL_H = 380,
     TK_PORT = 381,
     TK_WIDTH = 382,
     TK_JOB = 383,
     TK_DISTRIBUTE = 384,
     TK_VAL_M_STDEV = 385,
     TK_VOLT_M_STDEV = 386,
     TK_SLOPE_M_STDEV = 387,
     TK_VAL_H_STDEV = 388,
     TK_VOLT_H_STDEV = 389,
     TK_SLOPE_H_STDEV = 390,
     TK_NEG_HEB_PEAK_DELTA_USE = 391,
     TK_NEG_HEB_PEAK_TIME = 392,
     TK_VTAU_VOLT_M = 393,
     TK_POS_HEB_PEAK_DELTA_USE = 394,
     TK_POS_HEB_PEAK_TIME = 395,
     TK_VTAU_VOLT_H = 396,
     TK_INCLUDE = 397,
     TK_RSE_INIT = 398,
     TK_VERT_TRANS = 399,
     TK_PREV_SPIKE_RANGE = 400,
     TK_CONNECT_RPT = 401,
     TK_SPIKE_RPT = 402,
     TK_SERVER = 403,
     TK_SINGLE = 404,
     TK_CA_EXP_RANGE = 405,
     TK_PHASE_SHIFT = 406,
     TK_STRENGTH_RANGE = 407,
     TK_SYNAPSE_RSE = 408,
     TK_ALPHA_SCALE_H = 409,
     TK_ALPHA_SCALE_M = 410,
     TK_BETA_SCALE_H = 411,
     TK_BETA_SCALE_M = 412,
     TK_SAVE = 413,
     TK_LOAD = 414,
     TK_DISTANCE = 415,
     TK_OUTPUT_CONNECT_MAP = 416,
     TK_OUTPUT_CELLS = 417,
     TK_AUTO = 418,
     TK_SERVER_PORT = 419,
     TK_VERSION = 420,
     TK_SYNAPSE_UF = 421,
     TK_RECURRENT_CONNECT = 422,
     TK_ALPHA = 423,
     TK_SYN_AUGMENTATION = 424,
     TK_END_SYN_AUGMENTATION = 425,
     TK_MAX_AUGMENTATION = 426,
     TK_AUGMENTATION_INIT = 427,
     TK_AUGMENTATION_TAU = 428,
     TK_SYN_CALCIUM = 429,
     TK_CA_TAU_DECAY = 430,
     TK_EXP = 431,
     TK_SELECT_FRONT = 432,
     TK_OPTION = 433,
     TK_AVERAGE_SYN = 434,
     TK_AUGMENTATION_DELAY = 435,
     TK_WARNINGS_OFF = 436,
     TK_HIDE_TIMESTEP = 437,
     TK_HEBB_START = 438,
     TK_HEBB_END = 439,
     TK_EVENT = 440,
     TK_OVERRIDE = 441,
     TK_LEARN_SHAPE = 442,
     TK_RATE = 443,
     TK_TAU_NOISE = 444,
     TK_CORREL = 445,
     TK_END_EVENT = 446,
     TK_CELL_SEQUENCE = 447,
     TK_Km = 448,
     TK_Kahp = 449,
     TK_Ka = 450,
     TK_Na = 451,
     TK_Knicd = 452
   };
#endif



#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
typedef union YYSTYPE
{

/* Line 214 of yacc.c  */
#line 51 "parse.y"

  double rval;
  int    ival;
  char   sval [STRLEN];



/* Line 214 of yacc.c  */
#line 362 "parse.c"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif


/* Copy the second part of user declarations.  */


/* Line 264 of yacc.c  */
#line 374 "parse.c"

#ifdef short
# undef short
#endif

#ifdef YYTYPE_UINT8
typedef YYTYPE_UINT8 yytype_uint8;
#else
typedef unsigned char yytype_uint8;
#endif

#ifdef YYTYPE_INT8
typedef YYTYPE_INT8 yytype_int8;
#elif (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
typedef signed char yytype_int8;
#else
typedef short int yytype_int8;
#endif

#ifdef YYTYPE_UINT16
typedef YYTYPE_UINT16 yytype_uint16;
#else
typedef unsigned short int yytype_uint16;
#endif

#ifdef YYTYPE_INT16
typedef YYTYPE_INT16 yytype_int16;
#else
typedef short int yytype_int16;
#endif

#ifndef YYSIZE_T
# ifdef __SIZE_TYPE__
#  define YYSIZE_T __SIZE_TYPE__
# elif defined size_t
#  define YYSIZE_T size_t
# elif ! defined YYSIZE_T && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#  include <stddef.h> /* INFRINGES ON USER NAME SPACE */
#  define YYSIZE_T size_t
# else
#  define YYSIZE_T unsigned int
# endif
#endif

#define YYSIZE_MAXIMUM ((YYSIZE_T) -1)

#ifndef YY_
# if YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> /* INFRINGES ON USER NAME SPACE */
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

/* Suppress unused-variable warnings by "using" E.  */
#if ! defined lint || defined __GNUC__
# define YYUSE(e) ((void) (e))
#else
# define YYUSE(e) /* empty */
#endif

/* Identity function, used to suppress warnings about constant conditions.  */
#ifndef lint
# define YYID(n) (n)
#else
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static int
YYID (int yyi)
#else
static int
YYID (yyi)
    int yyi;
#endif
{
  return yyi;
}
#endif

#if ! defined yyoverflow || YYERROR_VERBOSE

/* The parser invokes alloca or malloc; define the necessary symbols.  */

# ifdef YYSTACK_USE_ALLOCA
#  if YYSTACK_USE_ALLOCA
#   ifdef __GNUC__
#    define YYSTACK_ALLOC __builtin_alloca
#   elif defined __BUILTIN_VA_ARG_INCR
#    include <alloca.h> /* INFRINGES ON USER NAME SPACE */
#   elif defined _AIX
#    define YYSTACK_ALLOC __alloca
#   elif defined _MSC_VER
#    include <malloc.h> /* INFRINGES ON USER NAME SPACE */
#    define alloca _alloca
#   else
#    define YYSTACK_ALLOC alloca
#    if ! defined _ALLOCA_H && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
#     include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#     ifndef _STDLIB_H
#      define _STDLIB_H 1
#     endif
#    endif
#   endif
#  endif
# endif

# ifdef YYSTACK_ALLOC
   /* Pacify GCC's `empty if-body' warning.  */
#  define YYSTACK_FREE(Ptr) do { /* empty */; } while (YYID (0))
#  ifndef YYSTACK_ALLOC_MAXIMUM
    /* The OS might guarantee only one guard page at the bottom of the stack,
       and a page size can be as small as 4096 bytes.  So we cannot safely
       invoke alloca (N) if N exceeds 4096.  Use a slightly smaller number
       to allow for a few compiler-allocated temporary stack slots.  */
#   define YYSTACK_ALLOC_MAXIMUM 4032 /* reasonable circa 2006 */
#  endif
# else
#  define YYSTACK_ALLOC YYMALLOC
#  define YYSTACK_FREE YYFREE
#  ifndef YYSTACK_ALLOC_MAXIMUM
#   define YYSTACK_ALLOC_MAXIMUM YYSIZE_MAXIMUM
#  endif
#  if (defined __cplusplus && ! defined _STDLIB_H \
       && ! ((defined YYMALLOC || defined malloc) \
	     && (defined YYFREE || defined free)))
#   include <stdlib.h> /* INFRINGES ON USER NAME SPACE */
#   ifndef _STDLIB_H
#    define _STDLIB_H 1
#   endif
#  endif
#  ifndef YYMALLOC
#   define YYMALLOC malloc
#   if ! defined malloc && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void *malloc (YYSIZE_T); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
#  ifndef YYFREE
#   define YYFREE free
#   if ! defined free && ! defined _STDLIB_H && (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
void free (void *); /* INFRINGES ON USER NAME SPACE */
#   endif
#  endif
# endif
#endif /* ! defined yyoverflow || YYERROR_VERBOSE */


#if (! defined yyoverflow \
     && (! defined __cplusplus \
	 || (defined YYSTYPE_IS_TRIVIAL && YYSTYPE_IS_TRIVIAL)))

/* A type that is properly aligned for any stack member.  */
union yyalloc
{
  yytype_int16 yyss_alloc;
  YYSTYPE yyvs_alloc;
};

/* The size of the maximum gap between one aligned stack and the next.  */
# define YYSTACK_GAP_MAXIMUM (sizeof (union yyalloc) - 1)

/* The size of an array large to enough to hold all stacks, each with
   N elements.  */
# define YYSTACK_BYTES(N) \
     ((N) * (sizeof (yytype_int16) + sizeof (YYSTYPE)) \
      + YYSTACK_GAP_MAXIMUM)

/* Copy COUNT objects from FROM to TO.  The source and destination do
   not overlap.  */
# ifndef YYCOPY
#  if defined __GNUC__ && 1 < __GNUC__
#   define YYCOPY(To, From, Count) \
      __builtin_memcpy (To, From, (Count) * sizeof (*(From)))
#  else
#   define YYCOPY(To, From, Count)		\
      do					\
	{					\
	  YYSIZE_T yyi;				\
	  for (yyi = 0; yyi < (Count); yyi++)	\
	    (To)[yyi] = (From)[yyi];		\
	}					\
      while (YYID (0))
#  endif
# endif

/* Relocate STACK from its old location to the new one.  The
   local variables YYSIZE and YYSTACKSIZE give the old and new number of
   elements in the stack, and YYPTR gives the new location of the
   stack.  Advance YYPTR to a properly aligned location for the next
   stack.  */
# define YYSTACK_RELOCATE(Stack_alloc, Stack)				\
    do									\
      {									\
	YYSIZE_T yynewbytes;						\
	YYCOPY (&yyptr->Stack_alloc, Stack, yysize);			\
	Stack = &yyptr->Stack_alloc;					\
	yynewbytes = yystacksize * sizeof (*Stack) + YYSTACK_GAP_MAXIMUM; \
	yyptr += yynewbytes / sizeof (*yyptr);				\
      }									\
    while (YYID (0))

#endif

/* YYFINAL -- State number of the termination state.  */
#define YYFINAL  66
/* YYLAST -- Last index in YYTABLE.  */
#define YYLAST   1253

/* YYNTOKENS -- Number of terminals.  */
#define YYNTOKENS  198
/* YYNNTS -- Number of nonterminals.  */
#define YYNNTS  171
/* YYNRULES -- Number of rules.  */
#define YYNRULES  422
/* YYNRULES -- Number of states.  */
#define YYNSTATES  749

/* YYTRANSLATE(YYLEX) -- Bison symbol number corresponding to YYLEX.  */
#define YYUNDEFTOK  2
#define YYMAXUTOK   452

#define YYTRANSLATE(YYX)						\
  ((unsigned int) (YYX) <= YYMAXUTOK ? yytranslate[YYX] : YYUNDEFTOK)

/* YYTRANSLATE[YYLEX] -- Bison symbol number corresponding to YYLEX.  */
static const yytype_uint8 yytranslate[] =
{
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33,    34,
      35,    36,    37,    38,    39,    40,    41,    42,    43,    44,
      45,    46,    47,    48,    49,    50,    51,    52,    53,    54,
      55,    56,    57,    58,    59,    60,    61,    62,    63,    64,
      65,    66,    67,    68,    69,    70,    71,    72,    73,    74,
      75,    76,    77,    78,    79,    80,    81,    82,    83,    84,
      85,    86,    87,    88,    89,    90,    91,    92,    93,    94,
      95,    96,    97,    98,    99,   100,   101,   102,   103,   104,
     105,   106,   107,   108,   109,   110,   111,   112,   113,   114,
     115,   116,   117,   118,   119,   120,   121,   122,   123,   124,
     125,   126,   127,   128,   129,   130,   131,   132,   133,   134,
     135,   136,   137,   138,   139,   140,   141,   142,   143,   144,
     145,   146,   147,   148,   149,   150,   151,   152,   153,   154,
     155,   156,   157,   158,   159,   160,   161,   162,   163,   164,
     165,   166,   167,   168,   169,   170,   171,   172,   173,   174,
     175,   176,   177,   178,   179,   180,   181,   182,   183,   184,
     185,   186,   187,   188,   189,   190,   191,   192,   193,   194,
     195,   196,   197
};

#if YYDEBUG
/* YYPRHS[YYN] -- Index of the first RHS symbol of rule number YYN in
   YYRHS.  */
static const yytype_uint16 yyprhs[] =
{
       0,     0,     3,     5,     8,    11,    13,    15,    17,    19,
      21,    23,    25,    27,    29,    31,    33,    35,    37,    39,
      41,    43,    45,    47,    49,    52,    53,    58,    60,    63,
      66,    69,    72,    74,    76,    79,    82,    85,    88,    91,
      94,   107,   121,   134,   137,   140,   143,   147,   150,   153,
     156,   159,   162,   165,   168,   171,   174,   177,   180,   181,
     186,   188,   191,   194,   197,   200,   204,   205,   210,   212,
     215,   218,   221,   224,   235,   247,   258,   259,   264,   266,
     269,   272,   275,   278,   279,   284,   286,   289,   292,   295,
     299,   308,   318,   327,   328,   333,   335,   338,   341,   347,
     354,   361,   362,   367,   369,   372,   375,   378,   381,   384,
     385,   389,   390,   394,   395,   399,   400,   404,   405,   409,
     410,   414,   415,   419,   420,   424,   425,   429,   430,   434,
     435,   439,   440,   446,   447,   453,   454,   460,   461,   467,
     468,   474,   476,   479,   482,   484,   487,   490,   492,   495,
     498,   500,   503,   506,   508,   511,   514,   515,   519,   520,
     524,   525,   529,   530,   534,   535,   539,   540,   544,   547,
     548,   552,   553,   557,   562,   565,   566,   570,   571,   575,
     576,   580,   581,   585,   586,   590,   591,   595,   596,   600,
     601,   605,   606,   610,   613,   616,   619,   622,   625,   628,
     631,   634,   635,   639,   640,   644,   645,   649,   650,   654,
     655,   659,   660,   664,   665,   669,   670,   674,   675,   679,
     680,   684,   688,   692,   695,   698,   699,   703,   704,   708,
     709,   713,   714,   718,   719,   724,   726,   729,   732,   735,
     738,   741,   744,   747,   750,   751,   755,   756,   760,   761,
     765,   766,   770,   771,   775,   776,   780,   783,   786,   787,
     792,   794,   797,   800,   803,   804,   809,   811,   814,   817,
     820,   823,   824,   828,   829,   833,   834,   839,   841,   844,
     847,   850,   853,   856,   857,   861,   862,   866,   867,   871,
     872,   876,   877,   881,   882,   886,   887,   892,   894,   897,
     900,   903,   904,   908,   909,   913,   914,   918,   919,   924,
     926,   929,   932,   933,   937,   938,   942,   943,   947,   948,
     952,   953,   957,   958,   962,   963,   967,   968,   972,   973,
     977,   978,   983,   985,   988,   991,   992,   996,   997,  1002,
    1004,  1007,  1010,  1013,  1016,  1019,  1022,  1025,  1028,  1031,
    1034,  1037,  1040,  1043,  1046,  1049,  1052,  1055,  1056,  1060,
    1061,  1065,  1068,  1071,  1074,  1077,  1078,  1082,  1083,  1087,
    1088,  1093,  1095,  1098,  1101,  1104,  1111,  1112,  1117,  1119,
    1122,  1125,  1131,  1134,  1137,  1140,  1142,  1145,  1148,  1151,
    1154,  1157,  1160,  1161,  1165,  1166,  1170,  1173,  1176,  1179,
    1182,  1185,  1188,  1191,  1194,  1197,  1198,  1203,  1205,  1208,
    1211,  1214,  1220,  1224,  1226,  1229,  1231,  1233,  1235,  1238,
    1241,  1243,  1245
};

/* YYRHS -- A `-1'-separated list of the rules' RHS.  */
static const yytype_int16 yyrhs[] =
{
     199,     0,    -1,   200,    -1,   199,   200,    -1,   199,     1,
      -1,   201,    -1,   209,    -1,   205,    -1,   217,    -1,   213,
      -1,   221,    -1,   225,    -1,   240,    -1,   287,    -1,   297,
      -1,   301,    -1,   307,    -1,   317,    -1,   324,    -1,   337,
      -1,   342,    -1,   350,    -1,   354,    -1,   360,    -1,   142,
       6,    -1,    -1,    11,   202,   203,    36,    -1,   204,    -1,
     203,   204,    -1,   119,     6,    -1,   128,     6,    -1,   129,
       6,    -1,   146,    -1,   147,    -1,    60,   368,    -1,    34,
     368,    -1,    94,     4,    -1,    27,     6,    -1,   102,     6,
      -1,    86,     6,    -1,    30,     6,     6,     6,     6,     6,
       6,     6,     6,     6,   368,   368,    -1,    30,     6,     6,
       6,     6,     6,     6,     6,     6,     6,   368,   368,   368,
      -1,   167,     6,     6,     6,     6,     6,     6,     6,     6,
       6,   368,   368,    -1,    66,     5,    -1,    64,     5,    -1,
      93,     6,    -1,   158,     6,   368,    -1,   159,     6,    -1,
     126,     4,    -1,   126,   163,    -1,   126,   149,    -1,   148,
       6,    -1,   164,     4,    -1,   160,     5,    -1,   162,     5,
      -1,   161,     5,    -1,   178,   181,    -1,   185,     6,    -1,
      -1,    26,   206,   207,    38,    -1,   208,    -1,   207,   208,
      -1,   119,     6,    -1,   127,   368,    -1,    61,   368,    -1,
      74,   368,   368,    -1,    -1,    25,   210,   211,    37,    -1,
     212,    -1,   211,   212,    -1,   119,     6,    -1,    26,     6,
      -1,    69,     6,    -1,    30,     6,     6,     6,     6,     6,
       6,     6,   368,   368,    -1,    30,     6,     6,     6,     6,
       6,     6,     6,   368,   368,   368,    -1,   167,     6,     6,
       6,     6,     6,     6,     6,   368,   368,    -1,    -1,    68,
     214,   215,    43,    -1,   216,    -1,   215,   216,    -1,   119,
       6,    -1,    75,   368,    -1,   120,   368,    -1,    -1,    67,
     218,   219,    42,    -1,   220,    -1,   219,   220,    -1,   119,
       6,    -1,    68,     6,    -1,    23,     6,     4,    -1,    30,
       6,     6,     6,     6,     6,   368,   368,    -1,    30,     6,
       6,     6,     6,     6,   368,   368,   368,    -1,   167,     6,
       6,     6,     6,     6,   368,   368,    -1,    -1,    20,   222,
     223,    40,    -1,   224,    -1,   223,   224,    -1,   119,     6,
      -1,    28,     6,     6,   368,   368,    -1,    28,     6,     6,
     368,   368,   368,    -1,    30,     6,     6,   368,   368,   368,
      -1,    -1,    28,   226,   227,    39,    -1,   228,    -1,   227,
     228,    -1,   119,     6,    -1,    94,     4,    -1,    99,     6,
      -1,    24,     6,    -1,    -1,   101,   229,   367,    -1,    -1,
     111,   230,   367,    -1,    -1,    91,   231,   367,    -1,    -1,
     114,   232,   367,    -1,    -1,    71,   233,   367,    -1,    -1,
      70,   234,   367,    -1,    -1,   122,   235,   367,    -1,    -1,
      15,   236,   367,    -1,    -1,    13,   237,   367,    -1,    -1,
      18,   238,   367,    -1,    -1,    17,   239,   367,    -1,    -1,
      24,   193,   241,   246,    41,    -1,    -1,    24,   194,   242,
     247,    41,    -1,    -1,    24,   195,   243,   248,    41,    -1,
      -1,    24,   196,   244,   249,    41,    -1,    -1,    24,   197,
     245,   250,    41,    -1,   251,    -1,   246,   251,    -1,   246,
     258,    -1,   251,    -1,   247,   251,    -1,   247,   261,    -1,
     251,    -1,   248,   251,    -1,   248,   267,    -1,   251,    -1,
     249,   251,    -1,   249,   276,    -1,   251,    -1,   250,   251,
      -1,   119,     6,    -1,    -1,    79,   252,   367,    -1,    -1,
     121,   253,   367,    -1,    -1,   105,   254,   367,    -1,    -1,
     152,   255,   367,    -1,    -1,    78,   256,   367,    -1,    -1,
      88,   257,   367,    -1,    94,     4,    -1,    -1,    54,   259,
     367,    -1,    -1,   112,   260,   367,    -1,    98,   368,   368,
     368,    -1,   132,   368,    -1,    -1,    16,   262,   367,    -1,
      -1,    12,   263,   367,    -1,    -1,   150,   264,   367,    -1,
      -1,    14,   265,   367,    -1,    -1,    19,   266,   367,    -1,
      -1,    62,   268,   367,    -1,    -1,    63,   269,   367,    -1,
      -1,    54,   270,   367,    -1,    -1,    53,   271,   367,    -1,
      98,   368,    -1,   132,   368,    -1,    97,   368,    -1,   135,
     368,    -1,   130,   368,    -1,   131,   368,    -1,   133,   368,
      -1,   134,   368,    -1,    -1,   124,   272,   366,    -1,    -1,
     138,   273,   366,    -1,    -1,   125,   274,   366,    -1,    -1,
     141,   275,   366,    -1,    -1,    54,   277,   367,    -1,    -1,
      53,   278,   367,    -1,    -1,    62,   279,   367,    -1,    -1,
      63,   280,   367,    -1,    -1,   112,   281,   367,    -1,    -1,
     113,   282,   367,    -1,    98,   368,   368,    -1,    97,   368,
     368,    -1,   132,   368,    -1,   135,   368,    -1,    -1,   155,
     283,   367,    -1,    -1,   157,   284,   367,    -1,    -1,   154,
     285,   367,    -1,    -1,   156,   286,   367,    -1,    -1,   104,
     288,   289,    48,    -1,   290,    -1,   289,   290,    -1,   119,
       6,    -1,    94,     4,    -1,    96,     6,    -1,    73,     6,
      -1,    31,     6,    -1,   169,     6,    -1,   109,     6,    -1,
      -1,     7,   291,   367,    -1,    -1,    32,   292,   367,    -1,
      -1,   110,   293,   367,    -1,    -1,    76,   294,   367,    -1,
      -1,   143,   295,   367,    -1,    -1,   145,   296,   367,    -1,
     183,   368,    -1,   184,   368,    -1,    -1,   109,   298,   299,
      51,    -1,   300,    -1,   299,   300,    -1,   119,     6,    -1,
      84,     6,    -1,    -1,   107,   302,   303,    50,    -1,   304,
      -1,   303,   304,    -1,   119,     6,    -1,    94,     4,    -1,
      95,     6,    -1,    -1,    55,   305,   367,    -1,    -1,    33,
     306,   367,    -1,    -1,   108,   308,   309,    52,    -1,   310,
      -1,   309,   310,    -1,   119,     6,    -1,    94,     4,    -1,
      72,     6,    -1,   187,     6,    -1,    -1,    80,   311,   367,
      -1,    -1,    82,   312,   367,    -1,    -1,   136,   313,   367,
      -1,    -1,   139,   314,   367,    -1,    -1,   137,   315,   367,
      -1,    -1,   140,   316,   367,    -1,    -1,   106,   318,   319,
      49,    -1,   320,    -1,   319,   320,    -1,   119,     6,    -1,
      94,     4,    -1,    -1,    76,   321,   367,    -1,    -1,    32,
     322,   367,    -1,    -1,   110,   323,   367,    -1,    -1,   169,
     325,   326,   170,    -1,   327,    -1,   326,   327,    -1,   119,
       6,    -1,    -1,    15,   328,   367,    -1,    -1,   175,   329,
     367,    -1,    -1,    18,   330,   367,    -1,    -1,    17,   331,
     367,    -1,    -1,   171,   332,   367,    -1,    -1,   168,   333,
     367,    -1,    -1,   172,   334,   367,    -1,    -1,   173,   335,
     367,    -1,    -1,   180,   336,   367,    -1,    -1,    99,   338,
     339,    45,    -1,   340,    -1,   339,   340,    -1,   119,     6,
      -1,    -1,   123,   341,   366,    -1,    -1,   100,   343,   344,
      46,    -1,   345,    -1,   344,   345,    -1,   119,     6,    -1,
      77,     6,    -1,    81,     6,    -1,   144,   368,    -1,   151,
     368,    -1,   188,   368,    -1,   189,   368,    -1,   190,   368,
      -1,   118,     6,    -1,    56,     6,    -1,   126,     4,    -1,
     126,   163,    -1,    92,     5,    -1,    94,     4,    -1,    58,
       4,    -1,    22,     4,    -1,    -1,   117,   346,   367,    -1,
      -1,    35,   347,   367,    -1,     9,   368,    -1,     8,   368,
      -1,   127,   368,    -1,    59,   368,    -1,    -1,   116,   348,
     366,    -1,    -1,   115,   349,   366,    -1,    -1,   102,   351,
     352,    47,    -1,   353,    -1,   352,   353,    -1,   119,     6,
      -1,   103,     6,    -1,    65,     6,     6,     6,     6,   368,
      -1,    -1,    86,   355,   356,    44,    -1,   357,    -1,   356,
     357,    -1,   119,     6,    -1,    21,     6,     6,     6,     6,
      -1,    56,     6,    -1,   126,     4,    -1,   126,   163,    -1,
      10,    -1,    10,   176,    -1,    24,     6,    -1,    87,     6,
      -1,   192,     6,    -1,    83,   368,    -1,    57,   368,    -1,
      -1,   116,   358,   366,    -1,    -1,   115,   359,   366,    -1,
     104,     6,    -1,   153,     6,    -1,   166,     6,    -1,   169,
       6,    -1,   174,     6,    -1,    94,     4,    -1,    94,   177,
      -1,   165,     4,    -1,   178,   364,    -1,    -1,   185,   361,
     362,   191,    -1,   363,    -1,   362,   363,    -1,   119,     6,
      -1,   104,     6,    -1,    21,     6,     6,     6,     6,    -1,
     186,     6,   368,    -1,   365,    -1,   364,   365,    -1,   179,
      -1,   182,    -1,   368,    -1,   366,   368,    -1,   368,   368,
      -1,   368,    -1,     4,    -1,     3,    -1
};

/* YYRLINE[YYN] -- source line where rule number YYN was defined.  */
static const yytype_uint16 yyrline[] =
{
       0,   121,   121,   122,   123,   126,   127,   128,   129,   130,
     131,   132,   133,   134,   135,   136,   137,   138,   139,   140,
     141,   142,   143,   144,   145,   150,   150,   153,   154,   157,
     158,   159,   160,   161,   162,   163,   164,   165,   167,   169,
     171,   177,   183,   194,   195,   196,   197,   198,   199,   200,
     201,   202,   203,   204,   205,   206,   207,   208,   213,   213,
     216,   217,   220,   221,   222,   223,   228,   228,   231,   232,
     235,   236,   237,   239,   245,   251,   262,   262,   265,   266,
     269,   270,   271,   276,   276,   279,   280,   283,   284,   285,
     287,   293,   299,   310,   310,   313,   314,   317,   318,   325,
     331,   340,   340,   343,   344,   347,   348,   349,   350,   352,
     352,   353,   353,   354,   354,   355,   355,   356,   356,   357,
     357,   358,   358,   359,   359,   360,   360,   361,   361,   362,
     362,   370,   370,   371,   371,   372,   372,   373,   373,   374,
     374,   377,   378,   379,   382,   383,   384,   387,   388,   389,
     392,   393,   394,   397,   398,   403,   404,   404,   405,   405,
     406,   406,   407,   407,   408,   408,   409,   409,   410,   413,
     413,   414,   414,   415,   418,   421,   421,   422,   422,   423,
     423,   424,   424,   425,   425,   428,   428,   429,   429,   430,
     430,   431,   431,   432,   433,   434,   435,   437,   438,   439,
     440,   442,   442,   443,   443,   444,   444,   445,   445,   448,
     448,   449,   449,   450,   450,   451,   451,   452,   452,   453,
     453,   454,   456,   458,   459,   460,   460,   461,   461,   462,
     462,   463,   463,   468,   468,   471,   472,   475,   476,   477,
     478,   479,   481,   482,   483,   483,   484,   484,   485,   485,
     486,   486,   487,   487,   488,   488,   489,   498,   511,   511,
     514,   515,   518,   519,   524,   524,   527,   528,   531,   532,
     533,   534,   534,   535,   535,   540,   540,   543,   544,   547,
     548,   549,   550,   551,   551,   552,   552,   553,   553,   554,
     554,   555,   555,   556,   556,   561,   561,   565,   566,   569,
     570,   571,   571,   572,   572,   573,   573,   578,   578,   581,
     582,   584,   585,   585,   586,   586,   587,   587,   588,   588,
     589,   589,   590,   590,   591,   591,   592,   592,   593,   593,
     598,   598,   601,   602,   605,   606,   606,   612,   612,   615,
     616,   619,   620,   621,   622,   623,   624,   625,   626,   627,
     628,   629,   630,   631,   632,   633,   634,   635,   635,   636,
     636,   637,   638,   639,   640,   641,   641,   643,   643,   649,
     649,   652,   653,   656,   657,   658,   668,   668,   671,   672,
     675,   676,   681,   682,   683,   684,   685,   687,   690,   691,
     692,   693,   694,   694,   697,   697,   700,   702,   706,   710,
     714,   718,   719,   720,   721,   724,   724,   727,   728,   731,
     732,   733,   739,   743,   744,   747,   748,   753,   754,   757,
     758,   761,   762
};
#endif

#if YYDEBUG || YYERROR_VERBOSE || YYTOKEN_TABLE
/* YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
   First, the terminals, then, starting at YYNTOKENS, nonterminals.  */
static const char *const yytname[] =
{
  "$end", "error", "$undefined", "REAL", "INTEGER", "LOGICAL", "NAME",
  "TK_ABSOLUTE_USE", "TK_AMP_END", "TK_AMP_START", "TK_ASCII", "TK_BRAIN",
  "TK_CA_EXP", "TK_CA_EXTERNAL", "TK_CA_HALF_MIN", "TK_CA_INTERNAL",
  "TK_CA_SCALE", "TK_CA_SPIKE_INC", "TK_CA_TAU", "TK_CA_TAU_SCALE",
  "TK_CELL", "TK_CELLS", "TK_CELLS_PER_FREQ", "TK_CELL_TYPE", "TK_CHANNEL",
  "TK_COLUMN", "TK_CSHELL", "TK_COLUMN_TYPE", "TK_CMP", "TK_G",
  "TK_CONNECT", "TK_DATA_LABEL", "TK_DELAY", "TK_DEPR_TAU", "TK_DURATION",
  "TK_DYN_RANGE", "TK_END_BRAIN", "TK_END_COLUMN", "TK_END_CSHELL",
  "TK_END_CMP", "TK_END_CELL", "TK_END_CHANNEL", "TK_END_LAYER",
  "TK_END_LSHELL", "TK_END_REPORT", "TK_END_SPIKE", "TK_END_STIMULUS",
  "TK_END_ST_INJECT", "TK_END_SYNAPSE", "TK_END_SYN_DATA", "TK_END_SYN_FD",
  "TK_END_SYN_PSG", "TK_END_SYN_LEARN", "TK_E_HALF_MIN_H",
  "TK_E_HALF_MIN_M", "TK_FACIL_TAU", "TK_FILENAME", "TK_FREQUENCY",
  "TK_FREQ_ROWS", "TK_FREQ_START", "TK_FSV", "TK_HEIGHT", "TK_H_INITIAL",
  "TK_H_POWER", "TK_IGNORE_EMPTY", "TK_INJECT", "TK_INTERACTIVE",
  "TK_LAYER", "TK_LSHELL", "TK_LAYER_TYPE", "TK_LEAK_G",
  "TK_LEAK_REVERSAL", "TK_LEARN", "TK_LEARN_LABEL", "TK_LOCATION",
  "TK_LOWER", "TK_MAX_G", "TK_MODE", "TK_M_INITIAL", "TK_M_POWER",
  "TK_NEG_HEB_WINDOW", "TK_PATTERN", "TK_POS_HEB_WINDOW", "TK_PROB",
  "TK_PSG_FILE", "TK_RELOAD_SYN", "TK_REPORT", "TK_REPORT_ON",
  "TK_REVERSAL", "TK_RSE", "TK_RSE_LABEL", "TK_R_MEMBRANE", "TK_SAMESEED",
  "TK_SAVE_SYN", "TK_SEED", "TK_SFD", "TK_SFD_LABEL", "TK_SLOPE_H",
  "TK_SLOPE_M", "TK_SPIKE", "TK_STIMULUS", "TK_SPIKE_HW", "TK_ST_INJECT",
  "TK_STIM_TYPE", "TK_SYNAPSE", "TK_STRENGTH", "TK_SYN_DATA", "TK_SYN_FD",
  "TK_SYN_LEARN", "TK_SYN_PSG", "TK_SYN_REVERSAL", "TK_TAU_MEMBRANE",
  "TK_TAU_SCALE_M", "TK_TAU_SCALE_H", "TK_THRESHOLD", "TK_TIME_END",
  "TK_TIME_START", "TK_TIME_FREQ_INC", "TK_TIMING", "TK_TYPE", "TK_UPPER",
  "TK_UNITARY_G", "TK_VMREST", "TK_VOLTAGES", "TK_VTAU_VAL_M",
  "TK_VTAU_VAL_H", "TK_PORT", "TK_WIDTH", "TK_JOB", "TK_DISTRIBUTE",
  "TK_VAL_M_STDEV", "TK_VOLT_M_STDEV", "TK_SLOPE_M_STDEV",
  "TK_VAL_H_STDEV", "TK_VOLT_H_STDEV", "TK_SLOPE_H_STDEV",
  "TK_NEG_HEB_PEAK_DELTA_USE", "TK_NEG_HEB_PEAK_TIME", "TK_VTAU_VOLT_M",
  "TK_POS_HEB_PEAK_DELTA_USE", "TK_POS_HEB_PEAK_TIME", "TK_VTAU_VOLT_H",
  "TK_INCLUDE", "TK_RSE_INIT", "TK_VERT_TRANS", "TK_PREV_SPIKE_RANGE",
  "TK_CONNECT_RPT", "TK_SPIKE_RPT", "TK_SERVER", "TK_SINGLE",
  "TK_CA_EXP_RANGE", "TK_PHASE_SHIFT", "TK_STRENGTH_RANGE",
  "TK_SYNAPSE_RSE", "TK_ALPHA_SCALE_H", "TK_ALPHA_SCALE_M",
  "TK_BETA_SCALE_H", "TK_BETA_SCALE_M", "TK_SAVE", "TK_LOAD",
  "TK_DISTANCE", "TK_OUTPUT_CONNECT_MAP", "TK_OUTPUT_CELLS", "TK_AUTO",
  "TK_SERVER_PORT", "TK_VERSION", "TK_SYNAPSE_UF", "TK_RECURRENT_CONNECT",
  "TK_ALPHA", "TK_SYN_AUGMENTATION", "TK_END_SYN_AUGMENTATION",
  "TK_MAX_AUGMENTATION", "TK_AUGMENTATION_INIT", "TK_AUGMENTATION_TAU",
  "TK_SYN_CALCIUM", "TK_CA_TAU_DECAY", "TK_EXP", "TK_SELECT_FRONT",
  "TK_OPTION", "TK_AVERAGE_SYN", "TK_AUGMENTATION_DELAY",
  "TK_WARNINGS_OFF", "TK_HIDE_TIMESTEP", "TK_HEBB_START", "TK_HEBB_END",
  "TK_EVENT", "TK_OVERRIDE", "TK_LEARN_SHAPE", "TK_RATE", "TK_TAU_NOISE",
  "TK_CORREL", "TK_END_EVENT", "TK_CELL_SEQUENCE", "TK_Km", "TK_Kahp",
  "TK_Ka", "TK_Na", "TK_Knicd", "$accept", "input", "element", "brain",
  "$@1", "brainvars", "brainvar", "colshell", "$@2", "cshvars", "cshvar",
  "column", "$@3", "colvars", "colvar", "lshell", "$@4", "lsvars", "lsvar",
  "layer", "$@5", "lvars", "lvar", "cell", "$@6", "cellvars", "cellvar",
  "compart", "$@7", "cmpvars", "cmpvar", "$@8", "$@9", "$@10", "$@11",
  "$@12", "$@13", "$@14", "$@15", "$@16", "$@17", "$@18", "channel",
  "$@19", "$@20", "$@21", "$@22", "$@23", "Kmvars", "Kahpvars", "Kavars",
  "Navars", "Knicdvars", "chvar", "$@24", "$@25", "$@26", "$@27", "$@28",
  "$@29", "Kmvar", "$@30", "$@31", "Kahpvar", "$@32", "$@33", "$@34",
  "$@35", "$@36", "Kavar", "$@37", "$@38", "$@39", "$@40", "$@41", "$@42",
  "$@43", "$@44", "Navar", "$@45", "$@46", "$@47", "$@48", "$@49", "$@50",
  "$@51", "$@52", "$@53", "$@54", "synapse", "$@55", "synvars", "synvar",
  "$@56", "$@57", "$@58", "$@59", "$@60", "$@61", "syn_psg", "$@62",
  "spvars", "spvar", "syn_fd", "$@63", "sfvars", "sfvar", "$@64", "$@65",
  "syn_learn", "$@66", "slvars", "slvar", "$@67", "$@68", "$@69", "$@70",
  "$@71", "$@72", "syn_data", "$@73", "sdvars", "sdvar", "$@74", "$@75",
  "$@76", "syn_augmentation", "$@77", "savars", "savar", "$@78", "$@79",
  "$@80", "$@81", "$@82", "$@83", "$@84", "$@85", "$@86", "spikeshape",
  "$@87", "spikevars", "spikevar", "$@88", "stimulus", "$@89", "stvars",
  "stvar", "$@90", "$@91", "$@92", "$@93", "stinject", "$@94", "stivars",
  "stivar", "report", "$@95", "reportvars", "reportvar", "$@96", "$@97",
  "event", "$@98", "eventvars", "eventvar", "reportoptions",
  "singleoption", "values", "twovalue", "value", 0
};
#endif

# ifdef YYPRINT
/* YYTOKNUM[YYLEX-NUM] -- Internal token number corresponding to
   token YYLEX-NUM.  */
static const yytype_uint16 yytoknum[] =
{
       0,   256,   257,   258,   259,   260,   261,   262,   263,   264,
     265,   266,   267,   268,   269,   270,   271,   272,   273,   274,
     275,   276,   277,   278,   279,   280,   281,   282,   283,   284,
     285,   286,   287,   288,   289,   290,   291,   292,   293,   294,
     295,   296,   297,   298,   299,   300,   301,   302,   303,   304,
     305,   306,   307,   308,   309,   310,   311,   312,   313,   314,
     315,   316,   317,   318,   319,   320,   321,   322,   323,   324,
     325,   326,   327,   328,   329,   330,   331,   332,   333,   334,
     335,   336,   337,   338,   339,   340,   341,   342,   343,   344,
     345,   346,   347,   348,   349,   350,   351,   352,   353,   354,
     355,   356,   357,   358,   359,   360,   361,   362,   363,   364,
     365,   366,   367,   368,   369,   370,   371,   372,   373,   374,
     375,   376,   377,   378,   379,   380,   381,   382,   383,   384,
     385,   386,   387,   388,   389,   390,   391,   392,   393,   394,
     395,   396,   397,   398,   399,   400,   401,   402,   403,   404,
     405,   406,   407,   408,   409,   410,   411,   412,   413,   414,
     415,   416,   417,   418,   419,   420,   421,   422,   423,   424,
     425,   426,   427,   428,   429,   430,   431,   432,   433,   434,
     435,   436,   437,   438,   439,   440,   441,   442,   443,   444,
     445,   446,   447,   448,   449,   450,   451,   452
};
# endif

/* YYR1[YYN] -- Symbol number of symbol that rule YYN derives.  */
static const yytype_uint16 yyr1[] =
{
       0,   198,   199,   199,   199,   200,   200,   200,   200,   200,
     200,   200,   200,   200,   200,   200,   200,   200,   200,   200,
     200,   200,   200,   200,   200,   202,   201,   203,   203,   204,
     204,   204,   204,   204,   204,   204,   204,   204,   204,   204,
     204,   204,   204,   204,   204,   204,   204,   204,   204,   204,
     204,   204,   204,   204,   204,   204,   204,   204,   206,   205,
     207,   207,   208,   208,   208,   208,   210,   209,   211,   211,
     212,   212,   212,   212,   212,   212,   214,   213,   215,   215,
     216,   216,   216,   218,   217,   219,   219,   220,   220,   220,
     220,   220,   220,   222,   221,   223,   223,   224,   224,   224,
     224,   226,   225,   227,   227,   228,   228,   228,   228,   229,
     228,   230,   228,   231,   228,   232,   228,   233,   228,   234,
     228,   235,   228,   236,   228,   237,   228,   238,   228,   239,
     228,   241,   240,   242,   240,   243,   240,   244,   240,   245,
     240,   246,   246,   246,   247,   247,   247,   248,   248,   248,
     249,   249,   249,   250,   250,   251,   252,   251,   253,   251,
     254,   251,   255,   251,   256,   251,   257,   251,   251,   259,
     258,   260,   258,   258,   258,   262,   261,   263,   261,   264,
     261,   265,   261,   266,   261,   268,   267,   269,   267,   270,
     267,   271,   267,   267,   267,   267,   267,   267,   267,   267,
     267,   272,   267,   273,   267,   274,   267,   275,   267,   277,
     276,   278,   276,   279,   276,   280,   276,   281,   276,   282,
     276,   276,   276,   276,   276,   283,   276,   284,   276,   285,
     276,   286,   276,   288,   287,   289,   289,   290,   290,   290,
     290,   290,   290,   290,   291,   290,   292,   290,   293,   290,
     294,   290,   295,   290,   296,   290,   290,   290,   298,   297,
     299,   299,   300,   300,   302,   301,   303,   303,   304,   304,
     304,   305,   304,   306,   304,   308,   307,   309,   309,   310,
     310,   310,   310,   311,   310,   312,   310,   313,   310,   314,
     310,   315,   310,   316,   310,   318,   317,   319,   319,   320,
     320,   321,   320,   322,   320,   323,   320,   325,   324,   326,
     326,   327,   328,   327,   329,   327,   330,   327,   331,   327,
     332,   327,   333,   327,   334,   327,   335,   327,   336,   327,
     338,   337,   339,   339,   340,   341,   340,   343,   342,   344,
     344,   345,   345,   345,   345,   345,   345,   345,   345,   345,
     345,   345,   345,   345,   345,   345,   345,   346,   345,   347,
     345,   345,   345,   345,   345,   348,   345,   349,   345,   351,
     350,   352,   352,   353,   353,   353,   355,   354,   356,   356,
     357,   357,   357,   357,   357,   357,   357,   357,   357,   357,
     357,   357,   358,   357,   359,   357,   357,   357,   357,   357,
     357,   357,   357,   357,   357,   361,   360,   362,   362,   363,
     363,   363,   363,   364,   364,   365,   365,   366,   366,   367,
     367,   368,   368
};

/* YYR2[YYN] -- Number of symbols composing right hand side of rule YYN.  */
static const yytype_uint8 yyr2[] =
{
       0,     2,     1,     2,     2,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     1,     1,     1,     1,     1,     1,
       1,     1,     1,     1,     2,     0,     4,     1,     2,     2,
       2,     2,     1,     1,     2,     2,     2,     2,     2,     2,
      12,    13,    12,     2,     2,     2,     3,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     0,     4,
       1,     2,     2,     2,     2,     3,     0,     4,     1,     2,
       2,     2,     2,    10,    11,    10,     0,     4,     1,     2,
       2,     2,     2,     0,     4,     1,     2,     2,     2,     3,
       8,     9,     8,     0,     4,     1,     2,     2,     5,     6,
       6,     0,     4,     1,     2,     2,     2,     2,     2,     0,
       3,     0,     3,     0,     3,     0,     3,     0,     3,     0,
       3,     0,     3,     0,     3,     0,     3,     0,     3,     0,
       3,     0,     5,     0,     5,     0,     5,     0,     5,     0,
       5,     1,     2,     2,     1,     2,     2,     1,     2,     2,
       1,     2,     2,     1,     2,     2,     0,     3,     0,     3,
       0,     3,     0,     3,     0,     3,     0,     3,     2,     0,
       3,     0,     3,     4,     2,     0,     3,     0,     3,     0,
       3,     0,     3,     0,     3,     0,     3,     0,     3,     0,
       3,     0,     3,     2,     2,     2,     2,     2,     2,     2,
       2,     0,     3,     0,     3,     0,     3,     0,     3,     0,
       3,     0,     3,     0,     3,     0,     3,     0,     3,     0,
       3,     3,     3,     2,     2,     0,     3,     0,     3,     0,
       3,     0,     3,     0,     4,     1,     2,     2,     2,     2,
       2,     2,     2,     2,     0,     3,     0,     3,     0,     3,
       0,     3,     0,     3,     0,     3,     2,     2,     0,     4,
       1,     2,     2,     2,     0,     4,     1,     2,     2,     2,
       2,     0,     3,     0,     3,     0,     4,     1,     2,     2,
       2,     2,     2,     0,     3,     0,     3,     0,     3,     0,
       3,     0,     3,     0,     3,     0,     4,     1,     2,     2,
       2,     0,     3,     0,     3,     0,     3,     0,     4,     1,
       2,     2,     0,     3,     0,     3,     0,     3,     0,     3,
       0,     3,     0,     3,     0,     3,     0,     3,     0,     3,
       0,     4,     1,     2,     2,     0,     3,     0,     4,     1,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     0,     3,     0,
       3,     2,     2,     2,     2,     0,     3,     0,     3,     0,
       4,     1,     2,     2,     2,     6,     0,     4,     1,     2,
       2,     5,     2,     2,     2,     1,     2,     2,     2,     2,
       2,     2,     0,     3,     0,     3,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     0,     4,     1,     2,     2,
       2,     5,     3,     1,     2,     1,     1,     1,     2,     2,
       1,     1,     1
};

/* YYDEFACT[STATE-NAME] -- Default rule to reduce with in state
   STATE-NUM when YYTABLE doesn't specify something else to do.  Zero
   means the default is an error.  */
static const yytype_uint16 yydefact[] =
{
       0,    25,    93,     0,    66,    58,   101,    83,    76,   376,
     330,   337,   369,   233,   295,   264,   275,   258,     0,   307,
     405,     0,     2,     5,     7,     6,     9,     8,    10,    11,
      12,    13,    14,    15,    16,    17,    18,    19,    20,    21,
      22,    23,     0,     0,   131,   133,   135,   137,   139,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    24,     0,     0,     1,     4,     3,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    32,    33,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,    27,     0,     0,     0,
       0,    95,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,     0,    68,     0,     0,     0,     0,     0,    60,
     125,   123,   129,   127,     0,   119,   117,   113,     0,     0,
     109,   111,   115,     0,   121,     0,   103,     0,     0,     0,
       0,     0,     0,    85,     0,     0,     0,     0,    78,   385,
       0,     0,     0,     0,     0,     0,     0,     0,   394,   392,
       0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     378,     0,   335,     0,   332,     0,     0,     0,   359,     0,
       0,     0,     0,     0,     0,     0,   367,   365,   357,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,   339,
       0,     0,     0,     0,   371,   244,     0,   246,     0,   250,
       0,     0,     0,   248,     0,   252,   254,     0,     0,     0,
       0,   235,   303,   301,     0,   305,     0,     0,   297,   273,
     271,     0,     0,     0,     0,   266,     0,   283,   285,     0,
       0,   287,   291,   289,   293,     0,     0,   277,     0,     0,
       0,   260,   312,   318,   316,     0,   322,   320,   324,   326,
     314,   328,     0,   309,     0,     0,     0,     0,     0,   407,
      37,     0,   422,   421,    35,    34,    44,    43,    39,    45,
      36,    38,    29,    48,    50,    49,    30,    31,    51,     0,
      47,    53,    55,    54,    52,     0,    56,    57,    26,    28,
       0,     0,    97,    94,    96,   164,   156,   166,     0,   160,
       0,   158,   162,     0,   141,     0,   144,     0,   147,     0,
     150,     0,   153,    71,     0,    72,    70,     0,    67,    69,
      64,     0,    62,    63,    59,    61,     0,     0,     0,     0,
     108,     0,     0,     0,   106,   107,     0,     0,     0,   105,
       0,   102,   104,     0,     0,    88,    87,     0,    84,    86,
      81,    80,    82,    77,    79,   386,     0,   387,   382,   391,
     390,   388,   401,   402,   396,     0,     0,   380,   383,   384,
     397,   403,   398,   399,   400,   415,   416,   404,   413,   389,
     377,   379,   334,     0,   331,   333,   362,   361,   356,     0,
     350,   355,   364,   342,   343,   353,   354,     0,     0,     0,
     349,   341,   351,   352,   363,   344,   345,   346,   347,   348,
     338,   340,     0,   374,   373,   370,   372,     0,   241,     0,
     240,     0,   238,   239,   243,     0,   237,     0,     0,   242,
     256,   257,   234,   236,     0,     0,   300,     0,   299,   296,
     298,     0,     0,   269,   270,   268,   265,   267,   281,     0,
       0,   280,   279,     0,     0,     0,     0,   282,   276,   278,
     263,   262,   259,   261,     0,     0,     0,   311,     0,     0,
       0,     0,     0,     0,   308,   310,     0,   410,   409,     0,
     406,   408,     0,    46,     0,     0,     0,     0,     0,     0,
     168,     0,   155,     0,     0,   132,   169,     0,   171,     0,
     142,   143,   177,   181,   175,   183,   134,   179,   145,   146,
     136,   191,   189,   185,   187,     0,     0,   201,   205,     0,
       0,     0,     0,     0,     0,   203,   207,   148,   149,   138,
     211,   209,   213,   215,     0,     0,   217,   219,     0,     0,
     229,   225,   231,   227,   151,   152,   140,   154,     0,     0,
      65,   126,   420,   124,   130,   128,   120,   118,   114,   110,
     112,   116,   122,    89,     0,     0,     0,   395,   417,   393,
     414,   336,   360,   368,   366,   358,     0,   245,   247,   251,
     249,   253,   255,   304,   302,   306,   274,   272,   284,   286,
     288,   292,   290,   294,   313,   319,   317,   323,   321,   325,
     327,   315,   329,     0,   412,     0,     0,     0,     0,   165,
     157,   167,   161,   159,   163,     0,     0,     0,   174,     0,
       0,     0,     0,     0,     0,     0,     0,     0,   195,   193,
       0,     0,   197,   198,   194,   199,   200,   196,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,   223,   224,
       0,     0,     0,     0,     0,     0,   419,     0,     0,     0,
     418,     0,     0,     0,     0,    98,     0,   170,     0,   172,
     178,   182,   176,   184,   180,   192,   190,   186,   188,   202,
     206,   204,   208,   212,   210,   214,   216,   222,   221,   218,
     220,   230,   226,   232,   228,     0,     0,     0,     0,   381,
       0,   411,     0,     0,    99,   100,   173,     0,     0,     0,
       0,   375,     0,     0,     0,     0,     0,     0,     0,     0,
       0,     0,    90,    92,     0,     0,     0,     0,    91,     0,
       0,    73,    75,     0,     0,    74,    40,    42,    41
};

/* YYDEFGOTO[NTERM-NUM].  */
static const yytype_int16 yydefgoto[] =
{
      -1,    21,    22,    23,    42,    95,    96,    24,    50,   118,
     119,    25,    49,   112,   113,    26,    53,   147,   148,    27,
      52,   142,   143,    28,    43,   100,   101,    29,    51,   135,
     136,   346,   347,   343,   348,   342,   341,   350,   337,   336,
     339,   338,    30,   102,   103,   104,   105,   106,   313,   315,
     317,   319,   321,   314,   498,   503,   501,   504,   497,   499,
     511,   625,   627,   519,   631,   629,   633,   630,   632,   538,
     636,   637,   635,   634,   640,   648,   641,   649,   555,   651,
     650,   652,   653,   656,   657,   661,   663,   660,   662,    31,
      58,   220,   221,   427,   429,   435,   431,   437,   438,    32,
      62,   250,   251,    33,    60,   234,   235,   452,   451,    34,
      61,   246,   247,   459,   460,   463,   465,   464,   466,    35,
      59,   227,   228,   445,   444,   447,    36,    64,   262,   263,
     474,   482,   476,   475,   479,   478,   480,   481,   483,    37,
      55,   173,   174,   393,    38,    56,   198,   199,   409,   399,
     408,   407,    39,    57,   203,   204,    40,    54,   169,   170,
     376,   375,    41,    65,   268,   269,   387,   388,   577,   561,
     562
};

/* YYPACT[STATE-NUM] -- Index in YYTABLE of the portion describing
   STATE-NUM.  */
#define YYPACT_NINF -375
static const yytype_int16 yypact[] =
{
     672,  -375,  -375,    93,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,    20,  -375,
    -375,    31,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,   899,   -17,  -375,  -375,  -375,  -375,  -375,    22,
      53,  1117,    47,   -55,   733,   -69,   408,    84,   250,    -7,
     164,   435,   -78,  -375,   135,     9,  -375,  -375,  -375,    29,
      32,    12,    12,    35,    40,    41,    56,    24,    57,    60,
       5,    61,    66,  -375,  -375,    68,    70,    72,    74,    76,
      91,    33,    94,   -74,   102,   794,  -375,   105,   113,   114,
      -1,  -375,   327,   327,   327,   327,   327,   123,   128,   137,
     138,   139,    23,  -375,    12,    12,   145,    12,   143,  -375,
    -375,  -375,  -375,  -375,   149,  -375,  -375,  -375,   155,   158,
    -375,  -375,  -375,   161,  -375,  1131,  -375,   169,   180,   187,
     202,   203,    38,  -375,    12,   209,    12,   159,  -375,    44,
     226,   230,   232,    12,    12,   237,     0,   243,  -375,  -375,
     247,     6,   255,   252,   257,   258,   262,  -165,   263,   669,
    -375,   265,  -375,    13,  -375,    12,    12,   269,  -375,   285,
     288,    12,   289,   291,   293,   297,  -375,  -375,  -375,   296,
     303,     8,    12,    12,    12,    12,    12,    12,   618,  -375,
     306,   307,   308,   177,  -375,  -375,   310,  -375,   313,  -375,
     316,   318,   322,  -375,   323,  -375,  -375,   324,    12,    12,
     245,  -375,  -375,  -375,   328,  -375,   325,   223,  -375,  -375,
    -375,   330,   329,   332,   146,  -375,   334,  -375,  -375,   339,
     341,  -375,  -375,  -375,  -375,   342,   400,  -375,   343,   344,
     -48,  -375,  -375,  -375,  -375,   345,  -375,  -375,  -375,  -375,
    -375,  -375,   -10,  -375,   346,   347,   350,   351,    -3,  -375,
    -375,   355,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,    12,
    -375,  -375,  -375,  -375,  -375,   356,  -375,  -375,  -375,  -375,
     357,   359,  -375,  -375,  -375,  -375,  -375,  -375,   362,  -375,
     361,  -375,  -375,  1074,  -375,   784,  -375,  1026,  -375,   943,
    -375,   206,  -375,  -375,   364,  -375,  -375,   365,  -375,  -375,
    -375,    12,  -375,  -375,  -375,  -375,    12,    12,    12,    12,
    -375,    12,    12,    12,  -375,  -375,    12,    12,    12,  -375,
      12,  -375,  -375,   369,   379,  -375,  -375,   380,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,   381,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,    12,    12,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -165,  -375,  -375,
    -375,  -375,  -375,    12,  -375,  -375,  -375,  -375,  -375,    12,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,    12,    12,    12,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,   383,  -375,  -375,  -375,  -375,    12,  -375,    12,
    -375,    12,  -375,  -375,  -375,    12,  -375,    12,    12,  -375,
    -375,  -375,  -375,  -375,    12,    12,  -375,    12,  -375,  -375,
    -375,    12,    12,  -375,  -375,  -375,  -375,  -375,  -375,    12,
      12,  -375,  -375,    12,    12,    12,    12,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,    12,    12,    12,  -375,    12,    12,
      12,    12,    12,    12,  -375,  -375,   385,  -375,  -375,    12,
    -375,  -375,   386,  -375,   388,    12,    12,    12,    12,    12,
    -375,    12,  -375,    12,    12,  -375,  -375,    12,  -375,    12,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,    12,    12,  -375,  -375,    12,
      12,    12,    12,    12,    12,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,    12,    12,  -375,  -375,    12,    12,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,   390,   395,
    -375,  -375,    12,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,   396,   405,   406,    12,  -375,    12,
    -375,    12,  -375,    12,    12,  -375,   407,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,   414,  -375,   416,   417,    12,    12,  -375,
    -375,  -375,  -375,  -375,  -375,    12,    12,    12,  -375,    12,
      12,    12,    12,    12,    12,    12,    12,    12,  -375,  -375,
      12,    12,  -375,  -375,  -375,  -375,  -375,  -375,    12,    12,
      12,    12,    12,    12,    12,    12,    12,    12,  -375,  -375,
      12,    12,    12,    12,   420,   421,  -375,   425,   429,   431,
    -375,   433,   434,   436,   438,    12,    12,  -375,    12,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,    12,
      12,    12,    12,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,   439,   441,   443,   444,  -375,
      12,  -375,   445,   447,  -375,  -375,  -375,   450,   451,    12,
      12,  -375,   459,   462,   463,   464,    12,    12,   465,   469,
      12,    12,    12,  -375,   470,   475,    12,    12,  -375,    12,
      12,    12,  -375,    12,    12,  -375,    12,  -375,  -375
};

/* YYPGOTO[NTERM-NUM].  */
static const yytype_int16 yypgoto[] =
{
    -375,  -375,   354,  -375,  -375,  -375,   273,  -375,  -375,  -375,
     227,  -375,  -375,  -375,   371,  -375,  -375,  -375,   294,  -375,
    -375,  -375,   348,  -375,  -375,  -375,   384,  -375,  -375,  -375,
     352,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,   -82,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,   266,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,   238,  -375,  -375,  -375,   259,  -375,  -375,  -375,
    -375,  -375,   246,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,   268,  -375,  -375,  -375,  -375,  -375,  -375,   234,
    -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,  -375,
    -375,  -375,   326,  -375,  -375,  -375,  -375,   299,  -375,  -375,
    -375,  -375,  -375,  -375,  -375,   295,  -375,  -375,  -375,   335,
    -375,  -375,  -375,  -375,  -375,   233,  -375,   116,  -374,  -253,
     -71
};

/* YYTABLE[YYPACT[STATE-NUM]].  What to do in state STATE-NUM.  If
   positive, shift that token.  If negative, reduce the rule which
   number is the opposite.  If zero, do what YYDEFACT says.
   If YYTABLE_NINF, syntax error.  */
#define YYTABLE_NINF -1
static const yytype_uint16 yytable[] =
{
     274,   275,   579,   472,   372,   252,   248,   253,   254,   283,
     378,    97,   412,    98,   385,   272,   273,   386,   264,   581,
     144,   316,   318,   320,   322,   222,    63,    97,   280,    98,
     264,    66,    67,   583,   584,   270,   248,   294,   271,   303,
     276,   249,     1,   330,   331,   277,   333,   278,   107,   107,
     171,     2,   108,   108,   172,     3,     4,     5,   394,     6,
     328,   137,   279,   281,   145,   146,   282,   286,   138,   223,
     137,   249,   287,   360,   288,   362,   289,   138,   290,   291,
     358,   292,   369,   370,   563,   564,   565,   224,   566,   567,
     568,   109,   109,   569,   570,   571,   293,   572,     7,     8,
     295,   265,    99,   225,   396,   397,   139,   296,   297,   255,
     402,   300,   226,   265,   114,   139,   266,     9,    99,   301,
     302,   414,   415,   416,   417,   418,   419,   115,   266,   323,
      10,    11,   171,    12,   324,    13,   172,    14,    15,    16,
      17,   110,   110,   325,   326,   327,   582,   440,   441,   200,
     252,   332,   253,   254,   284,   340,   585,   140,   256,   344,
     484,   257,   258,   259,   345,   260,   140,   349,   285,   379,
     261,   413,   116,    18,   587,   353,   588,   373,   589,   229,
     117,   334,   590,   267,   591,   592,   354,   201,   490,   111,
     111,   593,   594,   355,   595,   267,   456,   229,   596,   597,
      19,   230,   363,   202,   114,   141,   598,   599,   356,   357,
     600,   601,   602,   603,   141,   361,    20,   115,   493,   230,
     365,   604,   605,   606,   425,   607,   608,   609,   610,   611,
     612,   510,   366,   518,   144,   537,   367,   554,   368,   557,
     231,   232,   200,   371,   619,   620,   621,   556,   622,   374,
     623,   624,   205,   377,   255,   222,   381,   205,   231,   232,
     560,   380,   116,   382,   383,   233,   689,   690,   384,   389,
     117,   392,   449,   398,   691,   692,   206,   207,   145,   146,
     201,   206,   207,   233,   305,   306,    44,    45,    46,    47,
      48,   400,   401,   442,   307,   403,   202,   404,   405,   223,
     308,   406,   410,   256,   578,   578,   257,   258,   259,   411,
     260,   309,   422,   423,   424,   261,   428,   224,   208,   430,
     432,   209,   578,   208,   433,   310,   209,   311,   434,   436,
     439,   448,   446,   225,   453,   454,   578,   578,   455,   210,
     458,   211,   226,   461,   210,   335,   211,   462,   467,   470,
     471,   477,   486,   487,   212,   213,   488,   489,   312,   212,
     213,   492,   494,   495,   214,   496,   500,   502,   299,   214,
     558,   559,   677,   573,   679,    68,   680,   681,   682,   683,
     684,   685,   686,   687,   688,   574,   575,   576,   215,   586,
     216,   613,   615,   215,   616,   216,   664,   693,   694,   695,
     696,   665,   667,   699,   700,   305,   306,   701,   702,   703,
     704,   668,   669,   671,   217,   307,   175,   176,   614,   217,
     672,   308,   673,   674,   617,   618,   705,   706,   218,   219,
     177,   707,   309,   218,   219,   708,   626,   709,   628,   710,
     711,   364,   712,   178,   713,   717,   310,   718,   311,   719,
     720,   722,   468,   723,   638,   639,   724,   725,   642,   643,
     644,   645,   646,   647,   179,   728,   180,   181,   729,   730,
     731,   734,   236,   654,   655,   735,   739,   658,   659,   312,
     237,   740,   238,   329,   304,   182,   443,   352,   473,   183,
     359,   666,   469,   457,   239,   450,   485,   421,   426,   395,
     184,   491,   185,   580,   391,     0,   670,   236,   670,     0,
     670,     0,   670,   670,     0,   237,     0,   238,     0,   240,
       0,     0,     0,   186,   187,   188,   189,   190,     0,   239,
       0,     0,     0,     0,   191,   192,   241,   242,     0,   243,
     244,     0,     0,     0,     0,     0,   675,   676,     0,     0,
       0,     0,   193,     0,   240,   678,     0,     0,     0,   194,
       0,     0,     0,     0,     0,     0,     0,     0,     0,   578,
     578,   241,   242,     0,   243,   244,     0,   578,   578,     0,
       0,     0,     0,   697,   698,     0,     0,   245,     0,     0,
       0,     0,     0,     0,     0,     0,   195,   196,   197,     0,
       0,     0,     0,     0,   714,   715,     0,   716,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,   670,   670,
     670,   670,   245,     0,     0,     0,   175,   176,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,     0,   721,
     177,     0,     0,     0,     0,     0,     0,     0,   726,   727,
       0,     0,     0,   178,     0,   732,   733,     0,     0,   736,
     737,   738,     0,     0,   420,   741,   742,     0,   743,   744,
     745,     0,   746,   747,   179,   748,   180,   181,     0,   149,
       0,     0,     0,     1,     0,     0,     0,     0,     0,     0,
     150,     0,     2,   151,     0,   182,     3,     4,     5,   183,
       6,     0,     0,     0,     0,     0,     0,     0,     0,     0,
     184,     0,   185,   390,     0,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,   152,   153,     0,     0,     0,
       0,     0,     0,   186,   187,   188,   189,   190,     0,     7,
       8,     0,     0,   149,   191,   192,     0,     0,     0,     0,
       0,     0,   154,     0,   150,     0,   155,   151,     9,     0,
       0,     0,   193,   156,     0,     0,     0,     0,     0,   194,
       0,    10,    11,   157,    12,     0,    13,     0,    14,    15,
      16,    17,     0,     0,   158,   159,     0,     0,   160,   152,
     153,     0,     0,     0,     0,   161,   512,     0,   513,     0,
     514,     0,     0,   515,     0,     0,   195,   196,   197,     0,
       0,     0,     0,     0,    18,     0,   154,     0,     0,     0,
     155,    69,   162,     0,    70,   516,     0,   156,    71,     0,
     298,     0,     0,     0,   163,   164,     0,   157,   165,     0,
       0,    19,     0,   166,     0,     0,     0,   167,   158,   159,
       0,     0,   160,     0,    72,     0,     0,    20,    73,   161,
      74,   168,   305,   306,     0,     0,     0,     0,     0,     0,
       0,     0,   307,     0,     0,     0,     0,     0,   308,     0,
      75,     0,     0,     0,     0,     0,   162,    76,    77,   309,
       0,     0,     0,     0,     0,     0,    78,     0,   163,   164,
       0,     0,   165,   310,     0,   311,     0,   166,     0,     0,
       0,   167,     0,    79,     0,     0,     0,     0,     0,     0,
      80,     0,    81,    82,     0,   168,    69,     0,     0,    70,
       0,     0,     0,    71,   517,     0,   312,     0,     0,     0,
      83,    84,    85,     0,     0,     0,     0,     0,     0,     0,
       0,     0,    86,    87,    88,    89,    90,     0,    91,    72,
       0,    92,     0,    73,     0,    74,     0,     0,     0,     0,
       0,     0,    93,     0,     0,     0,     0,     0,     0,    94,
       0,     0,     0,     0,   539,    75,     0,     0,     0,     0,
       0,     0,    76,    77,     0,     0,   540,   541,     0,     0,
       0,    78,     0,     0,     0,   542,   543,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,    79,     0,
       0,   305,   306,     0,     0,    80,     0,    81,    82,     0,
       0,   307,     0,     0,     0,     0,     0,   308,     0,     0,
     544,   545,     0,     0,     0,    83,    84,    85,   309,     0,
       0,     0,     0,     0,     0,   546,   547,    86,    87,    88,
      89,    90,   310,    91,   311,     0,    92,   520,     0,     0,
       0,     0,     0,     0,     0,   548,     0,    93,   549,   521,
     522,     0,     0,     0,    94,     0,     0,     0,   523,   524,
       0,     0,     0,     0,     0,   312,     0,   550,   551,   552,
     553,     0,     0,     0,   305,   306,     0,     0,     0,     0,
       0,     0,     0,     0,   307,   505,     0,     0,     0,     0,
     308,     0,     0,   525,   526,     0,     0,     0,   506,     0,
     120,   309,   121,     0,   122,   123,     0,     0,     0,     0,
       0,   124,     0,     0,   120,   310,   121,   311,   122,   123,
     527,   528,   305,   306,     0,   124,   529,   530,   531,   532,
     533,   534,   307,     0,   535,     0,     0,   536,   308,     0,
     351,     0,   507,     0,     0,     0,     0,     0,   312,   309,
       0,     0,     0,     0,     0,     0,   508,   125,   126,     0,
       0,     0,     0,   310,     0,   311,     0,     0,     0,     0,
       0,   125,   126,     0,     0,     0,   509,     0,   127,     0,
       0,   128,     0,     0,     0,     0,   129,     0,   130,     0,
       0,     0,   127,     0,     0,   128,   312,     0,   131,     0,
     129,   132,   130,     0,     0,     0,   133,     0,     0,   134,
       0,     0,   131,     0,     0,   132,     0,     0,     0,     0,
     133,     0,     0,   134
};

static const yytype_int16 yycheck[] =
{
      71,    72,   376,    51,     4,    15,    84,    17,    18,     4,
       4,    28,     4,    30,   179,     3,     4,   182,    21,   393,
      75,   103,   104,   105,   106,    32,     6,    28,     4,    30,
      21,     0,     1,   407,   408,     6,    84,     4,     6,    40,
       5,   119,    11,   114,   115,     5,   117,     6,    26,    26,
     119,    20,    30,    30,   123,    24,    25,    26,    45,    28,
      37,    23,     6,     6,   119,   120,     6,     6,    30,    76,
      23,   119,     6,   144,     6,   146,     6,    30,     6,     5,
      42,     5,   153,   154,   337,   338,   339,    94,   341,   342,
     343,    69,    69,   346,   347,   348,     5,   350,    67,    68,
       6,   104,   119,   110,   175,   176,    68,   181,     6,   119,
     181,     6,   119,   104,    61,    68,   119,    86,   119,     6,
       6,   192,   193,   194,   195,   196,   197,    74,   119,     6,
      99,   100,   119,   102,     6,   104,   123,   106,   107,   108,
     109,   119,   119,     6,     6,     6,   399,   218,   219,    65,
      15,     6,    17,    18,   149,     6,   409,   119,   168,     4,
     170,   171,   172,   173,     6,   175,   119,     6,   163,   163,
     180,   163,   119,   142,   427,     6,   429,   177,   431,    33,
     127,    38,   435,   186,   437,   438,     6,   103,   191,   167,
     167,   444,   445,     6,   447,   186,    50,    33,   451,   452,
     169,    55,    43,   119,    61,   167,   459,   460,     6,     6,
     463,   464,   465,   466,   167,     6,   185,    74,   289,    55,
     176,   474,   475,   476,    47,   478,   479,   480,   481,   482,
     483,   313,     6,   315,    75,   317,     6,   319,     6,   321,
      94,    95,    65,     6,   497,   498,   499,    41,   501,     6,
     503,   504,     7,     6,   119,    32,     4,     7,    94,    95,
     331,     6,   119,     6,     6,   119,   640,   641,     6,     6,
     127,     6,    49,     4,   648,   649,    31,    32,   119,   120,
     103,    31,    32,   119,    78,    79,   193,   194,   195,   196,
     197,     6,     4,    48,    88,     6,   119,     6,     5,    76,
      94,     4,     6,   168,   375,   376,   171,   172,   173,     6,
     175,   105,     6,     6,     6,   180,     6,    94,    73,     6,
       4,    76,   393,    73,     6,   119,    76,   121,     6,     6,
       6,     6,     4,   110,     4,     6,   407,   408,     6,    94,
       6,    96,   119,     4,    94,   118,    96,     6,     6,     6,
       6,     6,     6,     6,   109,   110,     6,     6,   152,   109,
     110,     6,     6,     6,   119,     6,     4,     6,    95,   119,
       6,     6,   625,     4,   627,    21,   629,   630,   631,   632,
     633,   634,   635,   636,   637,     6,     6,     6,   143,     6,
     145,     6,     6,   143,     6,   145,     6,   650,   651,   652,
     653,     6,     6,   656,   657,    78,    79,   660,   661,   662,
     663,     6,     6,     6,   169,    88,     8,     9,   489,   169,
       6,    94,     6,     6,   495,   496,     6,     6,   183,   184,
      22,     6,   105,   183,   184,     6,   507,     6,   509,     6,
       6,   147,     6,    35,     6,     6,   119,     6,   121,     6,
       6,     6,    52,     6,   525,   526,     6,     6,   529,   530,
     531,   532,   533,   534,    56,     6,    58,    59,     6,     6,
       6,     6,    72,   544,   545,     6,     6,   548,   549,   152,
      80,     6,    82,   112,   100,    77,   220,   135,   250,    81,
     142,   562,   246,   234,    94,   227,   262,   198,   203,   173,
      92,   268,    94,   387,   169,    -1,   577,    72,   579,    -1,
     581,    -1,   583,   584,    -1,    80,    -1,    82,    -1,   119,
      -1,    -1,    -1,   115,   116,   117,   118,   119,    -1,    94,
      -1,    -1,    -1,    -1,   126,   127,   136,   137,    -1,   139,
     140,    -1,    -1,    -1,    -1,    -1,   617,   618,    -1,    -1,
      -1,    -1,   144,    -1,   119,   626,    -1,    -1,    -1,   151,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   640,
     641,   136,   137,    -1,   139,   140,    -1,   648,   649,    -1,
      -1,    -1,    -1,   654,   655,    -1,    -1,   187,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,   188,   189,   190,    -1,
      -1,    -1,    -1,    -1,   675,   676,    -1,   678,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   689,   690,
     691,   692,   187,    -1,    -1,    -1,     8,     9,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   710,
      22,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   719,   720,
      -1,    -1,    -1,    35,    -1,   726,   727,    -1,    -1,   730,
     731,   732,    -1,    -1,    46,   736,   737,    -1,   739,   740,
     741,    -1,   743,   744,    56,   746,    58,    59,    -1,    10,
      -1,    -1,    -1,    11,    -1,    -1,    -1,    -1,    -1,    -1,
      21,    -1,    20,    24,    -1,    77,    24,    25,    26,    81,
      28,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      92,    -1,    94,    44,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    56,    57,    -1,    -1,    -1,
      -1,    -1,    -1,   115,   116,   117,   118,   119,    -1,    67,
      68,    -1,    -1,    10,   126,   127,    -1,    -1,    -1,    -1,
      -1,    -1,    83,    -1,    21,    -1,    87,    24,    86,    -1,
      -1,    -1,   144,    94,    -1,    -1,    -1,    -1,    -1,   151,
      -1,    99,   100,   104,   102,    -1,   104,    -1,   106,   107,
     108,   109,    -1,    -1,   115,   116,    -1,    -1,   119,    56,
      57,    -1,    -1,    -1,    -1,   126,    12,    -1,    14,    -1,
      16,    -1,    -1,    19,    -1,    -1,   188,   189,   190,    -1,
      -1,    -1,    -1,    -1,   142,    -1,    83,    -1,    -1,    -1,
      87,    27,   153,    -1,    30,    41,    -1,    94,    34,    -1,
      36,    -1,    -1,    -1,   165,   166,    -1,   104,   169,    -1,
      -1,   169,    -1,   174,    -1,    -1,    -1,   178,   115,   116,
      -1,    -1,   119,    -1,    60,    -1,    -1,   185,    64,   126,
      66,   192,    78,    79,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    88,    -1,    -1,    -1,    -1,    -1,    94,    -1,
      86,    -1,    -1,    -1,    -1,    -1,   153,    93,    94,   105,
      -1,    -1,    -1,    -1,    -1,    -1,   102,    -1,   165,   166,
      -1,    -1,   169,   119,    -1,   121,    -1,   174,    -1,    -1,
      -1,   178,    -1,   119,    -1,    -1,    -1,    -1,    -1,    -1,
     126,    -1,   128,   129,    -1,   192,    27,    -1,    -1,    30,
      -1,    -1,    -1,    34,   150,    -1,   152,    -1,    -1,    -1,
     146,   147,   148,    -1,    -1,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,   158,   159,   160,   161,   162,    -1,   164,    60,
      -1,   167,    -1,    64,    -1,    66,    -1,    -1,    -1,    -1,
      -1,    -1,   178,    -1,    -1,    -1,    -1,    -1,    -1,   185,
      -1,    -1,    -1,    -1,    41,    86,    -1,    -1,    -1,    -1,
      -1,    -1,    93,    94,    -1,    -1,    53,    54,    -1,    -1,
      -1,   102,    -1,    -1,    -1,    62,    63,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   119,    -1,
      -1,    78,    79,    -1,    -1,   126,    -1,   128,   129,    -1,
      -1,    88,    -1,    -1,    -1,    -1,    -1,    94,    -1,    -1,
      97,    98,    -1,    -1,    -1,   146,   147,   148,   105,    -1,
      -1,    -1,    -1,    -1,    -1,   112,   113,   158,   159,   160,
     161,   162,   119,   164,   121,    -1,   167,    41,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,   132,    -1,   178,   135,    53,
      54,    -1,    -1,    -1,   185,    -1,    -1,    -1,    62,    63,
      -1,    -1,    -1,    -1,    -1,   152,    -1,   154,   155,   156,
     157,    -1,    -1,    -1,    78,    79,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    88,    41,    -1,    -1,    -1,    -1,
      94,    -1,    -1,    97,    98,    -1,    -1,    -1,    54,    -1,
      13,   105,    15,    -1,    17,    18,    -1,    -1,    -1,    -1,
      -1,    24,    -1,    -1,    13,   119,    15,   121,    17,    18,
     124,   125,    78,    79,    -1,    24,   130,   131,   132,   133,
     134,   135,    88,    -1,   138,    -1,    -1,   141,    94,    -1,
      39,    -1,    98,    -1,    -1,    -1,    -1,    -1,   152,   105,
      -1,    -1,    -1,    -1,    -1,    -1,   112,    70,    71,    -1,
      -1,    -1,    -1,   119,    -1,   121,    -1,    -1,    -1,    -1,
      -1,    70,    71,    -1,    -1,    -1,   132,    -1,    91,    -1,
      -1,    94,    -1,    -1,    -1,    -1,    99,    -1,   101,    -1,
      -1,    -1,    91,    -1,    -1,    94,   152,    -1,   111,    -1,
      99,   114,   101,    -1,    -1,    -1,   119,    -1,    -1,   122,
      -1,    -1,   111,    -1,    -1,   114,    -1,    -1,    -1,    -1,
     119,    -1,    -1,   122
};

/* YYSTOS[STATE-NUM] -- The (internal number of the) accessing
   symbol of state STATE-NUM.  */
static const yytype_uint16 yystos[] =
{
       0,    11,    20,    24,    25,    26,    28,    67,    68,    86,
      99,   100,   102,   104,   106,   107,   108,   109,   142,   169,
     185,   199,   200,   201,   205,   209,   213,   217,   221,   225,
     240,   287,   297,   301,   307,   317,   324,   337,   342,   350,
     354,   360,   202,   222,   193,   194,   195,   196,   197,   210,
     206,   226,   218,   214,   355,   338,   343,   351,   288,   318,
     302,   308,   298,     6,   325,   361,     0,     1,   200,    27,
      30,    34,    60,    64,    66,    86,    93,    94,   102,   119,
     126,   128,   129,   146,   147,   148,   158,   159,   160,   161,
     162,   164,   167,   178,   185,   203,   204,    28,    30,   119,
     223,   224,   241,   242,   243,   244,   245,    26,    30,    69,
     119,   167,   211,   212,    61,    74,   119,   127,   207,   208,
      13,    15,    17,    18,    24,    70,    71,    91,    94,    99,
     101,   111,   114,   119,   122,   227,   228,    23,    30,    68,
     119,   167,   219,   220,    75,   119,   120,   215,   216,    10,
      21,    24,    56,    57,    83,    87,    94,   104,   115,   116,
     119,   126,   153,   165,   166,   169,   174,   178,   192,   356,
     357,   119,   123,   339,   340,     8,     9,    22,    35,    56,
      58,    59,    77,    81,    92,    94,   115,   116,   117,   118,
     119,   126,   127,   144,   151,   188,   189,   190,   344,   345,
      65,   103,   119,   352,   353,     7,    31,    32,    73,    76,
      94,    96,   109,   110,   119,   143,   145,   169,   183,   184,
     289,   290,    32,    76,    94,   110,   119,   319,   320,    33,
      55,    94,    95,   119,   303,   304,    72,    80,    82,    94,
     119,   136,   137,   139,   140,   187,   309,   310,    84,   119,
     299,   300,    15,    17,    18,   119,   168,   171,   172,   173,
     175,   180,   326,   327,    21,   104,   119,   186,   362,   363,
       6,     6,     3,     4,   368,   368,     5,     5,     6,     6,
       4,     6,     6,     4,   149,   163,     6,     6,     6,     6,
       6,     5,     5,     5,     4,     6,   181,     6,    36,   204,
       6,     6,     6,    40,   224,    78,    79,    88,    94,   105,
     119,   121,   152,   246,   251,   247,   251,   248,   251,   249,
     251,   250,   251,     6,     6,     6,     6,     6,    37,   212,
     368,   368,     6,   368,    38,   208,   237,   236,   239,   238,
       6,   234,   233,   231,     4,     6,   229,   230,   232,     6,
     235,    39,   228,     6,     6,     6,     6,     6,    42,   220,
     368,     6,   368,    43,   216,   176,     6,     6,     6,   368,
     368,     6,     4,   177,     6,   359,   358,     6,     4,   163,
       6,     4,     6,     6,     6,   179,   182,   364,   365,     6,
      44,   357,     6,   341,    45,   340,   368,   368,     4,   347,
       6,     4,   368,     6,     6,     5,     4,   349,   348,   346,
       6,     6,     4,   163,   368,   368,   368,   368,   368,   368,
      46,   345,     6,     6,     6,    47,   353,   291,     6,   292,
       6,   294,     4,     6,     6,   293,     6,   295,   296,     6,
     368,   368,    48,   290,   322,   321,     4,   323,     6,    49,
     320,   306,   305,     4,     6,     6,    50,   304,     6,   311,
     312,     4,     6,   313,   315,   314,   316,     6,    52,   310,
       6,     6,    51,   300,   328,   331,   330,     6,   333,   332,
     334,   335,   329,   336,   170,   327,     6,     6,     6,     6,
     191,   363,     6,   368,     6,     6,     6,   256,   252,   257,
       4,   254,     6,   253,   255,    41,    54,    98,   112,   132,
     251,   258,    12,    14,    16,    19,    41,   150,   251,   261,
      41,    53,    54,    62,    63,    97,    98,   124,   125,   130,
     131,   132,   133,   134,   135,   138,   141,   251,   267,    41,
      53,    54,    62,    63,    97,    98,   112,   113,   132,   135,
     154,   155,   156,   157,   251,   276,    41,   251,     6,     6,
     368,   367,   368,   367,   367,   367,   367,   367,   367,   367,
     367,   367,   367,     4,     6,     6,     6,   366,   368,   366,
     365,   366,   367,   366,   366,   367,     6,   367,   367,   367,
     367,   367,   367,   367,   367,   367,   367,   367,   367,   367,
     367,   367,   367,   367,   367,   367,   367,   367,   367,   367,
     367,   367,   367,     6,   368,     6,     6,   368,   368,   367,
     367,   367,   367,   367,   367,   259,   368,   260,   368,   263,
     265,   262,   266,   264,   271,   270,   268,   269,   368,   368,
     272,   274,   368,   368,   368,   368,   368,   368,   273,   275,
     278,   277,   279,   280,   368,   368,   281,   282,   368,   368,
     285,   283,   286,   284,     6,     6,   368,     6,     6,     6,
     368,     6,     6,     6,     6,   368,   368,   367,   368,   367,
     367,   367,   367,   367,   367,   367,   367,   367,   367,   366,
     366,   366,   366,   367,   367,   367,   367,   368,   368,   367,
     367,   367,   367,   367,   367,     6,     6,     6,     6,     6,
       6,     6,     6,     6,   368,   368,   368,     6,     6,     6,
       6,   368,     6,     6,     6,     6,   368,   368,     6,     6,
       6,     6,   368,   368,     6,     6,   368,   368,   368,     6,
       6,   368,   368,   368,   368,   368,   368,   368,   368
};

#define yyerrok		(yyerrstatus = 0)
#define yyclearin	(yychar = YYEMPTY)
#define YYEMPTY		(-2)
#define YYEOF		0

#define YYACCEPT	goto yyacceptlab
#define YYABORT		goto yyabortlab
#define YYERROR		goto yyerrorlab


/* Like YYERROR except do call yyerror.  This remains here temporarily
   to ease the transition to the new meaning of YYERROR, for GCC.
   Once GCC version 2 has supplanted version 1, this can go.  */

#define YYFAIL		goto yyerrlab

#define YYRECOVERING()  (!!yyerrstatus)

#define YYBACKUP(Token, Value)					\
do								\
  if (yychar == YYEMPTY && yylen == 1)				\
    {								\
      yychar = (Token);						\
      yylval = (Value);						\
      yytoken = YYTRANSLATE (yychar);				\
      YYPOPSTACK (1);						\
      goto yybackup;						\
    }								\
  else								\
    {								\
      yyerror (YY_("syntax error: cannot back up")); \
      YYERROR;							\
    }								\
while (YYID (0))


#define YYTERROR	1
#define YYERRCODE	256


/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

#define YYRHSLOC(Rhs, K) ((Rhs)[K])
#ifndef YYLLOC_DEFAULT
# define YYLLOC_DEFAULT(Current, Rhs, N)				\
    do									\
      if (YYID (N))                                                    \
	{								\
	  (Current).first_line   = YYRHSLOC (Rhs, 1).first_line;	\
	  (Current).first_column = YYRHSLOC (Rhs, 1).first_column;	\
	  (Current).last_line    = YYRHSLOC (Rhs, N).last_line;		\
	  (Current).last_column  = YYRHSLOC (Rhs, N).last_column;	\
	}								\
      else								\
	{								\
	  (Current).first_line   = (Current).last_line   =		\
	    YYRHSLOC (Rhs, 0).last_line;				\
	  (Current).first_column = (Current).last_column =		\
	    YYRHSLOC (Rhs, 0).last_column;				\
	}								\
    while (YYID (0))
#endif


/* YY_LOCATION_PRINT -- Print the location on the stream.
   This macro was not mandated originally: define only if we know
   we won't break user code: when these are the locations we know.  */

#ifndef YY_LOCATION_PRINT
# if YYLTYPE_IS_TRIVIAL
#  define YY_LOCATION_PRINT(File, Loc)			\
     fprintf (File, "%d.%d-%d.%d",			\
	      (Loc).first_line, (Loc).first_column,	\
	      (Loc).last_line,  (Loc).last_column)
# else
#  define YY_LOCATION_PRINT(File, Loc) ((void) 0)
# endif
#endif


/* YYLEX -- calling `yylex' with the right arguments.  */

#ifdef YYLEX_PARAM
# define YYLEX yylex (YYLEX_PARAM)
#else
# define YYLEX yylex ()
#endif

/* Enable debugging if requested.  */
#if YYDEBUG

# ifndef YYFPRINTF
#  include <stdio.h> /* INFRINGES ON USER NAME SPACE */
#  define YYFPRINTF fprintf
# endif

# define YYDPRINTF(Args)			\
do {						\
  if (yydebug)					\
    YYFPRINTF Args;				\
} while (YYID (0))

# define YY_SYMBOL_PRINT(Title, Type, Value, Location)			  \
do {									  \
  if (yydebug)								  \
    {									  \
      YYFPRINTF (stderr, "%s ", Title);					  \
      yy_symbol_print (stderr,						  \
		  Type, Value); \
      YYFPRINTF (stderr, "\n");						  \
    }									  \
} while (YYID (0))


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_value_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_value_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (!yyvaluep)
    return;
# ifdef YYPRINT
  if (yytype < YYNTOKENS)
    YYPRINT (yyoutput, yytoknum[yytype], *yyvaluep);
# else
  YYUSE (yyoutput);
# endif
  switch (yytype)
    {
      default:
	break;
    }
}


/*--------------------------------.
| Print this symbol on YYOUTPUT.  |
`--------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_symbol_print (FILE *yyoutput, int yytype, YYSTYPE const * const yyvaluep)
#else
static void
yy_symbol_print (yyoutput, yytype, yyvaluep)
    FILE *yyoutput;
    int yytype;
    YYSTYPE const * const yyvaluep;
#endif
{
  if (yytype < YYNTOKENS)
    YYFPRINTF (yyoutput, "token %s (", yytname[yytype]);
  else
    YYFPRINTF (yyoutput, "nterm %s (", yytname[yytype]);

  yy_symbol_value_print (yyoutput, yytype, yyvaluep);
  YYFPRINTF (yyoutput, ")");
}

/*------------------------------------------------------------------.
| yy_stack_print -- Print the state stack from its BOTTOM up to its |
| TOP (included).                                                   |
`------------------------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_stack_print (yytype_int16 *yybottom, yytype_int16 *yytop)
#else
static void
yy_stack_print (yybottom, yytop)
    yytype_int16 *yybottom;
    yytype_int16 *yytop;
#endif
{
  YYFPRINTF (stderr, "Stack now");
  for (; yybottom <= yytop; yybottom++)
    {
      int yybot = *yybottom;
      YYFPRINTF (stderr, " %d", yybot);
    }
  YYFPRINTF (stderr, "\n");
}

# define YY_STACK_PRINT(Bottom, Top)				\
do {								\
  if (yydebug)							\
    yy_stack_print ((Bottom), (Top));				\
} while (YYID (0))


/*------------------------------------------------.
| Report that the YYRULE is going to be reduced.  |
`------------------------------------------------*/

#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yy_reduce_print (YYSTYPE *yyvsp, int yyrule)
#else
static void
yy_reduce_print (yyvsp, yyrule)
    YYSTYPE *yyvsp;
    int yyrule;
#endif
{
  int yynrhs = yyr2[yyrule];
  int yyi;
  unsigned long int yylno = yyrline[yyrule];
  YYFPRINTF (stderr, "Reducing stack by rule %d (line %lu):\n",
	     yyrule - 1, yylno);
  /* The symbols being reduced.  */
  for (yyi = 0; yyi < yynrhs; yyi++)
    {
      YYFPRINTF (stderr, "   $%d = ", yyi + 1);
      yy_symbol_print (stderr, yyrhs[yyprhs[yyrule] + yyi],
		       &(yyvsp[(yyi + 1) - (yynrhs)])
		       		       );
      YYFPRINTF (stderr, "\n");
    }
}

# define YY_REDUCE_PRINT(Rule)		\
do {					\
  if (yydebug)				\
    yy_reduce_print (yyvsp, Rule); \
} while (YYID (0))

/* Nonzero means print parse trace.  It is left uninitialized so that
   multiple parsers can coexist.  */
int yydebug;
#else /* !YYDEBUG */
# define YYDPRINTF(Args)
# define YY_SYMBOL_PRINT(Title, Type, Value, Location)
# define YY_STACK_PRINT(Bottom, Top)
# define YY_REDUCE_PRINT(Rule)
#endif /* !YYDEBUG */


/* YYINITDEPTH -- initial size of the parser's stacks.  */
#ifndef	YYINITDEPTH
# define YYINITDEPTH 200
#endif

/* YYMAXDEPTH -- maximum size the stacks can grow to (effective only
   if the built-in stack extension method is used).

   Do not make this value too large; the results are undefined if
   YYSTACK_ALLOC_MAXIMUM < YYSTACK_BYTES (YYMAXDEPTH)
   evaluated with infinite-precision integer arithmetic.  */

#ifndef YYMAXDEPTH
# define YYMAXDEPTH 10000
#endif



#if YYERROR_VERBOSE

# ifndef yystrlen
#  if defined __GLIBC__ && defined _STRING_H
#   define yystrlen strlen
#  else
/* Return the length of YYSTR.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static YYSIZE_T
yystrlen (const char *yystr)
#else
static YYSIZE_T
yystrlen (yystr)
    const char *yystr;
#endif
{
  YYSIZE_T yylen;
  for (yylen = 0; yystr[yylen]; yylen++)
    continue;
  return yylen;
}
#  endif
# endif

# ifndef yystpcpy
#  if defined __GLIBC__ && defined _STRING_H && defined _GNU_SOURCE
#   define yystpcpy stpcpy
#  else
/* Copy YYSRC to YYDEST, returning the address of the terminating '\0' in
   YYDEST.  */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static char *
yystpcpy (char *yydest, const char *yysrc)
#else
static char *
yystpcpy (yydest, yysrc)
    char *yydest;
    const char *yysrc;
#endif
{
  char *yyd = yydest;
  const char *yys = yysrc;

  while ((*yyd++ = *yys++) != '\0')
    continue;

  return yyd - 1;
}
#  endif
# endif

# ifndef yytnamerr
/* Copy to YYRES the contents of YYSTR after stripping away unnecessary
   quotes and backslashes, so that it's suitable for yyerror.  The
   heuristic is that double-quoting is unnecessary unless the string
   contains an apostrophe, a comma, or backslash (other than
   backslash-backslash).  YYSTR is taken from yytname.  If YYRES is
   null, do not copy; instead, return the length of what the result
   would have been.  */
static YYSIZE_T
yytnamerr (char *yyres, const char *yystr)
{
  if (*yystr == '"')
    {
      YYSIZE_T yyn = 0;
      char const *yyp = yystr;

      for (;;)
	switch (*++yyp)
	  {
	  case '\'':
	  case ',':
	    goto do_not_strip_quotes;

	  case '\\':
	    if (*++yyp != '\\')
	      goto do_not_strip_quotes;
	    /* Fall through.  */
	  default:
	    if (yyres)
	      yyres[yyn] = *yyp;
	    yyn++;
	    break;

	  case '"':
	    if (yyres)
	      yyres[yyn] = '\0';
	    return yyn;
	  }
    do_not_strip_quotes: ;
    }

  if (! yyres)
    return yystrlen (yystr);

  return yystpcpy (yyres, yystr) - yyres;
}
# endif

/* Copy into YYRESULT an error message about the unexpected token
   YYCHAR while in state YYSTATE.  Return the number of bytes copied,
   including the terminating null byte.  If YYRESULT is null, do not
   copy anything; just return the number of bytes that would be
   copied.  As a special case, return 0 if an ordinary "syntax error"
   message will do.  Return YYSIZE_MAXIMUM if overflow occurs during
   size calculation.  */
static YYSIZE_T
yysyntax_error (char *yyresult, int yystate, int yychar)
{
  int yyn = yypact[yystate];

  if (! (YYPACT_NINF < yyn && yyn <= YYLAST))
    return 0;
  else
    {
      int yytype = YYTRANSLATE (yychar);
      YYSIZE_T yysize0 = yytnamerr (0, yytname[yytype]);
      YYSIZE_T yysize = yysize0;
      YYSIZE_T yysize1;
      int yysize_overflow = 0;
      enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
      char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];
      int yyx;

# if 0
      /* This is so xgettext sees the translatable formats that are
	 constructed on the fly.  */
      YY_("syntax error, unexpected %s");
      YY_("syntax error, unexpected %s, expecting %s");
      YY_("syntax error, unexpected %s, expecting %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s");
      YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s");
# endif
      char *yyfmt;
      char const *yyf;
      static char const yyunexpected[] = "syntax error, unexpected %s";
      static char const yyexpecting[] = ", expecting %s";
      static char const yyor[] = " or %s";
      char yyformat[sizeof yyunexpected
		    + sizeof yyexpecting - 1
		    + ((YYERROR_VERBOSE_ARGS_MAXIMUM - 2)
		       * (sizeof yyor - 1))];
      char const *yyprefix = yyexpecting;

      /* Start YYX at -YYN if negative to avoid negative indexes in
	 YYCHECK.  */
      int yyxbegin = yyn < 0 ? -yyn : 0;

      /* Stay within bounds of both yycheck and yytname.  */
      int yychecklim = YYLAST - yyn + 1;
      int yyxend = yychecklim < YYNTOKENS ? yychecklim : YYNTOKENS;
      int yycount = 1;

      yyarg[0] = yytname[yytype];
      yyfmt = yystpcpy (yyformat, yyunexpected);

      for (yyx = yyxbegin; yyx < yyxend; ++yyx)
	if (yycheck[yyx + yyn] == yyx && yyx != YYTERROR)
	  {
	    if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
	      {
		yycount = 1;
		yysize = yysize0;
		yyformat[sizeof yyunexpected - 1] = '\0';
		break;
	      }
	    yyarg[yycount++] = yytname[yyx];
	    yysize1 = yysize + yytnamerr (0, yytname[yyx]);
	    yysize_overflow |= (yysize1 < yysize);
	    yysize = yysize1;
	    yyfmt = yystpcpy (yyfmt, yyprefix);
	    yyprefix = yyor;
	  }

      yyf = YY_(yyformat);
      yysize1 = yysize + yystrlen (yyf);
      yysize_overflow |= (yysize1 < yysize);
      yysize = yysize1;

      if (yysize_overflow)
	return YYSIZE_MAXIMUM;

      if (yyresult)
	{
	  /* Avoid sprintf, as that infringes on the user's name space.
	     Don't have undefined behavior even if the translation
	     produced a string with the wrong number of "%s"s.  */
	  char *yyp = yyresult;
	  int yyi = 0;
	  while ((*yyp = *yyf) != '\0')
	    {
	      if (*yyp == '%' && yyf[1] == 's' && yyi < yycount)
		{
		  yyp += yytnamerr (yyp, yyarg[yyi++]);
		  yyf += 2;
		}
	      else
		{
		  yyp++;
		  yyf++;
		}
	    }
	}
      return yysize;
    }
}
#endif /* YYERROR_VERBOSE */


/*-----------------------------------------------.
| Release the memory associated to this symbol.  |
`-----------------------------------------------*/

/*ARGSUSED*/
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
static void
yydestruct (const char *yymsg, int yytype, YYSTYPE *yyvaluep)
#else
static void
yydestruct (yymsg, yytype, yyvaluep)
    const char *yymsg;
    int yytype;
    YYSTYPE *yyvaluep;
#endif
{
  YYUSE (yyvaluep);

  if (!yymsg)
    yymsg = "Deleting";
  YY_SYMBOL_PRINT (yymsg, yytype, yyvaluep, yylocationp);

  switch (yytype)
    {

      default:
	break;
    }
}

/* Prevent warnings from -Wmissing-prototypes.  */
#ifdef YYPARSE_PARAM
#if defined __STDC__ || defined __cplusplus
int yyparse (void *YYPARSE_PARAM);
#else
int yyparse ();
#endif
#else /* ! YYPARSE_PARAM */
#if defined __STDC__ || defined __cplusplus
int yyparse (void);
#else
int yyparse ();
#endif
#endif /* ! YYPARSE_PARAM */


/* The lookahead symbol.  */
int yychar;

/* The semantic value of the lookahead symbol.  */
YYSTYPE yylval;

/* Number of syntax errors so far.  */
int yynerrs;



/*-------------------------.
| yyparse or yypush_parse.  |
`-------------------------*/

#ifdef YYPARSE_PARAM
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void *YYPARSE_PARAM)
#else
int
yyparse (YYPARSE_PARAM)
    void *YYPARSE_PARAM;
#endif
#else /* ! YYPARSE_PARAM */
#if (defined __STDC__ || defined __C99__FUNC__ \
     || defined __cplusplus || defined _MSC_VER)
int
yyparse (void)
#else
int
yyparse ()

#endif
#endif
{


    int yystate;
    /* Number of tokens to shift before error messages enabled.  */
    int yyerrstatus;

    /* The stacks and their tools:
       `yyss': related to states.
       `yyvs': related to semantic values.

       Refer to the stacks thru separate pointers, to allow yyoverflow
       to reallocate them elsewhere.  */

    /* The state stack.  */
    yytype_int16 yyssa[YYINITDEPTH];
    yytype_int16 *yyss;
    yytype_int16 *yyssp;

    /* The semantic value stack.  */
    YYSTYPE yyvsa[YYINITDEPTH];
    YYSTYPE *yyvs;
    YYSTYPE *yyvsp;

    YYSIZE_T yystacksize;

  int yyn;
  int yyresult;
  /* Lookahead token as an internal (translated) token number.  */
  int yytoken;
  /* The variables used to return semantic value and location from the
     action routines.  */
  YYSTYPE yyval;

#if YYERROR_VERBOSE
  /* Buffer for error messages, and its allocated size.  */
  char yymsgbuf[128];
  char *yymsg = yymsgbuf;
  YYSIZE_T yymsg_alloc = sizeof yymsgbuf;
#endif

#define YYPOPSTACK(N)   (yyvsp -= (N), yyssp -= (N))

  /* The number of symbols on the RHS of the reduced rule.
     Keep to zero when no symbol should be popped.  */
  int yylen = 0;

  yytoken = 0;
  yyss = yyssa;
  yyvs = yyvsa;
  yystacksize = YYINITDEPTH;

  YYDPRINTF ((stderr, "Starting parse\n"));

  yystate = 0;
  yyerrstatus = 0;
  yynerrs = 0;
  yychar = YYEMPTY; /* Cause a token to be read.  */

  /* Initialize stack pointers.
     Waste one element of value and location stack
     so that they stay on the same level as the state stack.
     The wasted elements are never initialized.  */
  yyssp = yyss;
  yyvsp = yyvs;

  goto yysetstate;

/*------------------------------------------------------------.
| yynewstate -- Push a new state, which is found in yystate.  |
`------------------------------------------------------------*/
 yynewstate:
  /* In all cases, when you get here, the value and location stacks
     have just been pushed.  So pushing a state here evens the stacks.  */
  yyssp++;

 yysetstate:
  *yyssp = yystate;

  if (yyss + yystacksize - 1 <= yyssp)
    {
      /* Get the current used size of the three stacks, in elements.  */
      YYSIZE_T yysize = yyssp - yyss + 1;

#ifdef yyoverflow
      {
	/* Give user a chance to reallocate the stack.  Use copies of
	   these so that the &'s don't force the real ones into
	   memory.  */
	YYSTYPE *yyvs1 = yyvs;
	yytype_int16 *yyss1 = yyss;

	/* Each stack pointer address is followed by the size of the
	   data in use in that stack, in bytes.  This used to be a
	   conditional around just the two extra args, but that might
	   be undefined if yyoverflow is a macro.  */
	yyoverflow (YY_("memory exhausted"),
		    &yyss1, yysize * sizeof (*yyssp),
		    &yyvs1, yysize * sizeof (*yyvsp),
		    &yystacksize);

	yyss = yyss1;
	yyvs = yyvs1;
      }
#else /* no yyoverflow */
# ifndef YYSTACK_RELOCATE
      goto yyexhaustedlab;
# else
      /* Extend the stack our own way.  */
      if (YYMAXDEPTH <= yystacksize)
	goto yyexhaustedlab;
      yystacksize *= 2;
      if (YYMAXDEPTH < yystacksize)
	yystacksize = YYMAXDEPTH;

      {
	yytype_int16 *yyss1 = yyss;
	union yyalloc *yyptr =
	  (union yyalloc *) YYSTACK_ALLOC (YYSTACK_BYTES (yystacksize));
	if (! yyptr)
	  goto yyexhaustedlab;
	YYSTACK_RELOCATE (yyss_alloc, yyss);
	YYSTACK_RELOCATE (yyvs_alloc, yyvs);
#  undef YYSTACK_RELOCATE
	if (yyss1 != yyssa)
	  YYSTACK_FREE (yyss1);
      }
# endif
#endif /* no yyoverflow */

      yyssp = yyss + yysize - 1;
      yyvsp = yyvs + yysize - 1;

      YYDPRINTF ((stderr, "Stack size increased to %lu\n",
		  (unsigned long int) yystacksize));

      if (yyss + yystacksize - 1 <= yyssp)
	YYABORT;
    }

  YYDPRINTF ((stderr, "Entering state %d\n", yystate));

  if (yystate == YYFINAL)
    YYACCEPT;

  goto yybackup;

/*-----------.
| yybackup.  |
`-----------*/
yybackup:

  /* Do appropriate processing given the current state.  Read a
     lookahead token if we need one and don't already have one.  */

  /* First try to decide what to do without reference to lookahead token.  */
  yyn = yypact[yystate];
  if (yyn == YYPACT_NINF)
    goto yydefault;

  /* Not known => get a lookahead token if don't already have one.  */

  /* YYCHAR is either YYEMPTY or YYEOF or a valid lookahead symbol.  */
  if (yychar == YYEMPTY)
    {
      YYDPRINTF ((stderr, "Reading a token: "));
      yychar = YYLEX;
    }

  if (yychar <= YYEOF)
    {
      yychar = yytoken = YYEOF;
      YYDPRINTF ((stderr, "Now at end of input.\n"));
    }
  else
    {
      yytoken = YYTRANSLATE (yychar);
      YY_SYMBOL_PRINT ("Next token is", yytoken, &yylval, &yylloc);
    }

  /* If the proper action on seeing token YYTOKEN is to reduce or to
     detect an error, take that action.  */
  yyn += yytoken;
  if (yyn < 0 || YYLAST < yyn || yycheck[yyn] != yytoken)
    goto yydefault;
  yyn = yytable[yyn];
  if (yyn <= 0)
    {
      if (yyn == 0 || yyn == YYTABLE_NINF)
	goto yyerrlab;
      yyn = -yyn;
      goto yyreduce;
    }

  /* Count tokens shifted since error; after three, turn off error
     status.  */
  if (yyerrstatus)
    yyerrstatus--;

  /* Shift the lookahead token.  */
  YY_SYMBOL_PRINT ("Shifting", yytoken, &yylval, &yylloc);

  /* Discard the shifted token.  */
  yychar = YYEMPTY;

  yystate = yyn;
  *++yyvsp = yylval;

  goto yynewstate;


/*-----------------------------------------------------------.
| yydefault -- do the default action for the current state.  |
`-----------------------------------------------------------*/
yydefault:
  yyn = yydefact[yystate];
  if (yyn == 0)
    goto yyerrlab;
  goto yyreduce;


/*-----------------------------.
| yyreduce -- Do a reduction.  |
`-----------------------------*/
yyreduce:
  /* yyn is the number of a rule to reduce with.  */
  yylen = yyr2[yyn];

  /* If YYLEN is nonzero, implement the default value of the action:
     `$$ = $1'.

     Otherwise, the following line sets YYVAL to garbage.
     This behavior is undocumented and Bison
     users should not rely upon it.  Assigning to YYVAL
     unconditionally makes the parser a bit smaller, and it avoids a
     GCC warning that YYVAL may be used uninitialized.  */
  yyval = yyvsp[1-yylen];


  YY_REDUCE_PRINT (yyn);
  switch (yyn)
    {
        case 24:

/* Line 1455 of yacc.c  */
#line 145 "parse.y"
    { multiInput( (yyvsp[(2) - (2)].sval) ); ;}
    break;

  case 25:

/* Line 1455 of yacc.c  */
#line 150 "parse.y"
    { brain = makebrain (); ;}
    break;

  case 29:

/* Line 1455 of yacc.c  */
#line 157 "parse.y"
    { brain->L.name      = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 30:

/* Line 1455 of yacc.c  */
#line 158 "parse.y"
    { brain->job         = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 31:

/* Line 1455 of yacc.c  */
#line 159 "parse.y"
    { brain->distribute  = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 32:

/* Line 1455 of yacc.c  */
#line 160 "parse.y"
    { brain->ConnectRpt  = TRUE; ;}
    break;

  case 33:

/* Line 1455 of yacc.c  */
#line 161 "parse.y"
    { brain->SpikeRpt    = TRUE; ;}
    break;

  case 34:

/* Line 1455 of yacc.c  */
#line 162 "parse.y"
    { brain->FSV         = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 35:

/* Line 1455 of yacc.c  */
#line 163 "parse.y"
    { brain->Duration    = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 36:

/* Line 1455 of yacc.c  */
#line 164 "parse.y"
    { brain->Seed        = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 37:

/* Line 1455 of yacc.c  */
#line 165 "parse.y"
    { brain->ColumnNames = AddName (brain->ColumnNames, (yyvsp[(2) - (2)].sval), 0);
                                     brain->nColumns++; ;}
    break;

  case 38:

/* Line 1455 of yacc.c  */
#line 167 "parse.y"
    { brain->StInjNames  = AddName (brain->StInjNames,  (yyvsp[(2) - (2)].sval), 0);
                                     brain->nStInject++; ;}
    break;

  case 39:

/* Line 1455 of yacc.c  */
#line 169 "parse.y"
    { brain->ReportNames = AddName (brain->ReportNames, (yyvsp[(2) - (2)].sval), 0);
                                     brain->nReports++; ;}
    break;

  case 40:

/* Line 1455 of yacc.c  */
#line 172 "parse.y"
    { brain->CnList = makeConnect (brain->CnList, &(brain->nConnect),
                                               (yyvsp[(2) - (12)].sval), (yyvsp[(3) - (12)].sval), (yyvsp[(4) - (12)].sval), (yyvsp[(5) - (12)].sval),
                                               (yyvsp[(6) - (12)].sval), (yyvsp[(7) - (12)].sval), (yyvsp[(8) - (12)].sval), (yyvsp[(9) - (12)].sval),
                                               (yyvsp[(10) - (12)].sval), (yyvsp[(11) - (12)].rval), (yyvsp[(12) - (12)].rval));
               ;}
    break;

  case 41:

/* Line 1455 of yacc.c  */
#line 178 "parse.y"
    { brain->CnList = makeDecayingConnect ( brain->CnList, &(brain->nConnect),
                                               (yyvsp[(2) - (13)].sval), (yyvsp[(3) - (13)].sval), (yyvsp[(4) - (13)].sval), (yyvsp[(5) - (13)].sval),
                                               (yyvsp[(6) - (13)].sval), (yyvsp[(7) - (13)].sval), (yyvsp[(8) - (13)].sval), (yyvsp[(9) - (13)].sval),
                                               (yyvsp[(10) - (13)].sval), (yyvsp[(11) - (13)].rval), (yyvsp[(12) - (13)].rval), (yyvsp[(13) - (13)].rval) );
               ;}
    break;

  case 42:

/* Line 1455 of yacc.c  */
#line 184 "parse.y"
    {
                 brain->recurrentList = makeRecurrentConnect( brain->recurrentList, &(brain->nRecurrent),
                                               (yyvsp[(2) - (12)].sval), (yyvsp[(3) - (12)].sval), (yyvsp[(4) - (12)].sval), (yyvsp[(5) - (12)].sval),
                                               (yyvsp[(6) - (12)].sval), (yyvsp[(7) - (12)].sval), (yyvsp[(8) - (12)].sval), (yyvsp[(9) - (12)].sval),
                                               (yyvsp[(10) - (12)].sval),
 (yyvsp[(11) - (12)].rval),
 (yyvsp[(12) - (12)].rval)
 );
               ;}
    break;

  case 43:

/* Line 1455 of yacc.c  */
#line 194 "parse.y"
    { unused (TK_INTERACTIVE); ;}
    break;

  case 44:

/* Line 1455 of yacc.c  */
#line 195 "parse.y"
    { unused (TK_IGNORE_EMPTY); ;}
    break;

  case 45:

/* Line 1455 of yacc.c  */
#line 196 "parse.y"
    { unused (TK_SAVE_SYN); ;}
    break;

  case 46:

/* Line 1455 of yacc.c  */
#line 197 "parse.y"
    { brain->savefile = strdup( (yyvsp[(2) - (3)].sval) ); brain->savetime = (yyvsp[(3) - (3)].rval); ;}
    break;

  case 47:

/* Line 1455 of yacc.c  */
#line 198 "parse.y"
    { brain->loadfile = strdup( (yyvsp[(2) - (2)].sval) ); ;}
    break;

  case 48:

/* Line 1455 of yacc.c  */
#line 199 "parse.y"
    { brain->Port = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 49:

/* Line 1455 of yacc.c  */
#line 200 "parse.y"
    { brain->Port = -1; ;}
    break;

  case 50:

/* Line 1455 of yacc.c  */
#line 201 "parse.y"
    { brain->Port = -2; ;}
    break;

  case 51:

/* Line 1455 of yacc.c  */
#line 202 "parse.y"
    { brain->HostName = strdup( (yyvsp[(2) - (2)].sval) ); ;}
    break;

  case 52:

/* Line 1455 of yacc.c  */
#line 203 "parse.y"
    { brain->HostPort = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 53:

/* Line 1455 of yacc.c  */
#line 204 "parse.y"
    { if( (yyvsp[(2) - (2)].ival) ) brain->flag = setFlag( brain->flag, "USE_DISTANCE" ); ;}
    break;

  case 54:

/* Line 1455 of yacc.c  */
#line 205 "parse.y"
    { if( (yyvsp[(2) - (2)].ival) ) brain->flag = setFlag( brain->flag, "OUTPUT_CELLS" ); ;}
    break;

  case 55:

/* Line 1455 of yacc.c  */
#line 206 "parse.y"
    { if( (yyvsp[(2) - (2)].ival) ) brain->flag = setFlag( brain->flag, "OUTPUT_CONNECT_MAP" ); ;}
    break;

  case 56:

/* Line 1455 of yacc.c  */
#line 207 "parse.y"
    { brain->flag = setFlag( brain->flag, "WARNINGS_OFF" );  ;}
    break;

  case 57:

/* Line 1455 of yacc.c  */
#line 208 "parse.y"
    { brain->EventNames = AddName( brain->EventNames, (yyvsp[(2) - (2)].sval), 0 ); brain->nEvents++; ;}
    break;

  case 58:

/* Line 1455 of yacc.c  */
#line 213 "parse.y"
    { csh = makecsh (); ;}
    break;

  case 62:

/* Line 1455 of yacc.c  */
#line 220 "parse.y"
    { csh->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 63:

/* Line 1455 of yacc.c  */
#line 221 "parse.y"
    { csh->width  = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 64:

/* Line 1455 of yacc.c  */
#line 222 "parse.y"
    { csh->height = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 65:

/* Line 1455 of yacc.c  */
#line 223 "parse.y"
    { csh->x      = (yyvsp[(2) - (3)].rval); csh->y = (yyvsp[(3) - (3)].rval); ;}
    break;

  case 66:

/* Line 1455 of yacc.c  */
#line 228 "parse.y"
    { column = makecolumn (); ;}
    break;

  case 70:

/* Line 1455 of yacc.c  */
#line 235 "parse.y"
    { column->L.name     = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 71:

/* Line 1455 of yacc.c  */
#line 236 "parse.y"
    { column->shellName  = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 72:

/* Line 1455 of yacc.c  */
#line 237 "parse.y"
    { column->LayerNames = AddName (column->LayerNames, (yyvsp[(2) - (2)].sval), 0);
                             column->nLayers++; ;}
    break;

  case 73:

/* Line 1455 of yacc.c  */
#line 240 "parse.y"
    { column->CnList = makeConnect (column->CnList, &(column->nConnect),
                                                NULL, (yyvsp[(2) - (10)].sval), (yyvsp[(3) - (10)].sval), (yyvsp[(4) - (10)].sval),
                                                NULL, (yyvsp[(5) - (10)].sval), (yyvsp[(6) - (10)].sval), (yyvsp[(7) - (10)].sval),
                                                (yyvsp[(8) - (10)].sval), (yyvsp[(9) - (10)].rval), (yyvsp[(10) - (10)].rval));
               ;}
    break;

  case 74:

/* Line 1455 of yacc.c  */
#line 246 "parse.y"
    { column->CnList = makeDecayingConnect (column->CnList, &(column->nConnect),
                                                NULL, (yyvsp[(2) - (11)].sval), (yyvsp[(3) - (11)].sval), (yyvsp[(4) - (11)].sval),
                                                NULL, (yyvsp[(5) - (11)].sval), (yyvsp[(6) - (11)].sval), (yyvsp[(7) - (11)].sval),
                                                (yyvsp[(8) - (11)].sval), (yyvsp[(9) - (11)].rval), (yyvsp[(10) - (11)].rval), (yyvsp[(11) - (11)].rval));
               ;}
    break;

  case 75:

/* Line 1455 of yacc.c  */
#line 252 "parse.y"
    {
                 column->recurrentList = makeRecurrentConnect( column->recurrentList, &(column->nRecurrent),
                                               NULL, (yyvsp[(2) - (10)].sval), (yyvsp[(3) - (10)].sval), (yyvsp[(4) - (10)].sval),
                                               NULL, (yyvsp[(5) - (10)].sval), (yyvsp[(6) - (10)].sval), (yyvsp[(7) - (10)].sval),
                                               (yyvsp[(8) - (10)].sval), (yyvsp[(9) - (10)].rval), (yyvsp[(10) - (10)].rval) );
               ;}
    break;

  case 76:

/* Line 1455 of yacc.c  */
#line 262 "parse.y"
    { lsh = makelsh (); ;}
    break;

  case 80:

/* Line 1455 of yacc.c  */
#line 269 "parse.y"
    { lsh->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 81:

/* Line 1455 of yacc.c  */
#line 270 "parse.y"
    { lsh->Lower  = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 82:

/* Line 1455 of yacc.c  */
#line 271 "parse.y"
    { lsh->Upper  = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 83:

/* Line 1455 of yacc.c  */
#line 276 "parse.y"
    { layer = makelayer (); ;}
    break;

  case 87:

/* Line 1455 of yacc.c  */
#line 283 "parse.y"
    { layer->L.name    = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 88:

/* Line 1455 of yacc.c  */
#line 284 "parse.y"
    { layer->shellName = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 89:

/* Line 1455 of yacc.c  */
#line 285 "parse.y"
    { layer->CellNames = AddName (layer->CellNames, (yyvsp[(2) - (3)].sval), (int) (yyvsp[(3) - (3)].ival));
                                     layer->nCellTypes++; ;}
    break;

  case 90:

/* Line 1455 of yacc.c  */
#line 288 "parse.y"
    { layer->CnList = makeConnect (layer->CnList, &(layer->nConnect),
                                               NULL, NULL, (yyvsp[(2) - (8)].sval), (yyvsp[(3) - (8)].sval),
                                               NULL, NULL, (yyvsp[(4) - (8)].sval), (yyvsp[(5) - (8)].sval),
                                               (yyvsp[(6) - (8)].sval), (yyvsp[(7) - (8)].rval), (yyvsp[(8) - (8)].rval));
               ;}
    break;

  case 91:

/* Line 1455 of yacc.c  */
#line 294 "parse.y"
    { layer->CnList = makeDecayingConnect (layer->CnList, &(layer->nConnect),
                                               NULL, NULL, (yyvsp[(2) - (9)].sval), (yyvsp[(3) - (9)].sval),
                                               NULL, NULL, (yyvsp[(4) - (9)].sval), (yyvsp[(5) - (9)].sval),
                                               (yyvsp[(6) - (9)].sval), (yyvsp[(7) - (9)].rval), (yyvsp[(8) - (9)].rval), (yyvsp[(9) - (9)].rval));
               ;}
    break;

  case 92:

/* Line 1455 of yacc.c  */
#line 300 "parse.y"
    {
                 layer->recurrentList = makeRecurrentConnect( layer->recurrentList, &(layer->nRecurrent), 
                                               NULL, NULL, (yyvsp[(2) - (8)].sval), (yyvsp[(3) - (8)].sval),
                                               NULL, NULL, (yyvsp[(4) - (8)].sval), (yyvsp[(5) - (8)].sval),
                                               (yyvsp[(6) - (8)].sval), (yyvsp[(7) - (8)].rval), (yyvsp[(8) - (8)].rval) );
               ;}
    break;

  case 93:

/* Line 1455 of yacc.c  */
#line 310 "parse.y"
    { cell = makecell (); ;}
    break;

  case 97:

/* Line 1455 of yacc.c  */
#line 317 "parse.y"
    { cell->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 98:

/* Line 1455 of yacc.c  */
#line 319 "parse.y"
    { cell->CmpNames = AddCmp (cell->CmpNames, (yyvsp[(2) - (5)].sval), (yyvsp[(3) - (5)].sval),
                                                     (yyvsp[(4) - (5)].rval), (yyvsp[(5) - (5)].rval), 0);
                            //pass 0 for z-coord for compatibility ------^
                            //with older input files
                            cell->nCmp++;
                          ;}
    break;

  case 99:

/* Line 1455 of yacc.c  */
#line 326 "parse.y"
    { cell->CmpNames = AddCmp (cell->CmpNames, (yyvsp[(2) - (6)].sval), (yyvsp[(3) - (6)].sval),
                                                     (yyvsp[(4) - (6)].rval), (yyvsp[(5) - (6)].rval), (yyvsp[(6) - (6)].rval) );
                            cell->nCmp++;
                          ;}
    break;

  case 100:

/* Line 1455 of yacc.c  */
#line 332 "parse.y"
    { cell->CnList = makeCmpConn (cell->CnList, (yyvsp[(2) - (6)].sval), (yyvsp[(3) - (6)].sval), 
                                                         (yyvsp[(4) - (6)].rval), (yyvsp[(5) - (6)].rval), (yyvsp[(6) - (6)].rval)); 
                            cell->nConnect++;
                          ;}
    break;

  case 101:

/* Line 1455 of yacc.c  */
#line 340 "parse.y"
    { cmp = makecmp (); ;}
    break;

  case 105:

/* Line 1455 of yacc.c  */
#line 347 "parse.y"
    { cmp->L.name     = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 106:

/* Line 1455 of yacc.c  */
#line 348 "parse.y"
    { cmp->Seed       = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 107:

/* Line 1455 of yacc.c  */
#line 349 "parse.y"
    { cmp->SpikeName  = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 108:

/* Line 1455 of yacc.c  */
#line 350 "parse.y"
    { cmp->ChannelNames = AddName (cmp->ChannelNames, (yyvsp[(2) - (2)].sval), 0);
                                     cmp->nChannels++; ;}
    break;

  case 109:

/* Line 1455 of yacc.c  */
#line 352 "parse.y"
    { twoptr = cmp->Spike_HW; ;}
    break;

  case 111:

/* Line 1455 of yacc.c  */
#line 353 "parse.y"
    { twoptr = cmp->Tau_Membrane; ;}
    break;

  case 113:

/* Line 1455 of yacc.c  */
#line 354 "parse.y"
    { twoptr = cmp->R_Membrane; ;}
    break;

  case 115:

/* Line 1455 of yacc.c  */
#line 355 "parse.y"
    { twoptr = cmp->Threshold; ;}
    break;

  case 117:

/* Line 1455 of yacc.c  */
#line 356 "parse.y"
    { twoptr = cmp->Leak_Reversal; ;}
    break;

  case 119:

/* Line 1455 of yacc.c  */
#line 357 "parse.y"
    { twoptr = cmp->Leak_G; ;}
    break;

  case 121:

/* Line 1455 of yacc.c  */
#line 358 "parse.y"
    { twoptr = cmp->VMREST; ;}
    break;

  case 123:

/* Line 1455 of yacc.c  */
#line 359 "parse.y"
    { twoptr = cmp->CaInt; ;}
    break;

  case 125:

/* Line 1455 of yacc.c  */
#line 360 "parse.y"
    { twoptr = cmp->CaExt; ;}
    break;

  case 127:

/* Line 1455 of yacc.c  */
#line 361 "parse.y"
    { twoptr = cmp->CaTau; ;}
    break;

  case 129:

/* Line 1455 of yacc.c  */
#line 362 "parse.y"
    { twoptr = cmp->CaSpikeInc; ;}
    break;

  case 131:

/* Line 1455 of yacc.c  */
#line 370 "parse.y"
    { chan = makechan ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 133:

/* Line 1455 of yacc.c  */
#line 371 "parse.y"
    { chan = makechan ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 135:

/* Line 1455 of yacc.c  */
#line 372 "parse.y"
    { chan = makechan ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 137:

/* Line 1455 of yacc.c  */
#line 373 "parse.y"
    { chan = makechan ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 139:

/* Line 1455 of yacc.c  */
#line 374 "parse.y"
    { chan = makechan ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 155:

/* Line 1455 of yacc.c  */
#line 403 "parse.y"
    { chan->L.name    = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 156:

/* Line 1455 of yacc.c  */
#line 404 "parse.y"
    { twoptr = chan->mPower; ;}
    break;

  case 158:

/* Line 1455 of yacc.c  */
#line 405 "parse.y"
    { twoptr = chan->unitaryG; ;}
    break;

  case 160:

/* Line 1455 of yacc.c  */
#line 406 "parse.y"
    { twoptr = chan->strength ; ;}
    break;

  case 162:

/* Line 1455 of yacc.c  */
#line 407 "parse.y"
    { twoptr = chan->strength_range; ;}
    break;

  case 164:

/* Line 1455 of yacc.c  */
#line 408 "parse.y"
    { twoptr = chan->M_Initial; ;}
    break;

  case 166:

/* Line 1455 of yacc.c  */
#line 409 "parse.y"
    { twoptr = chan->ReversePot; ;}
    break;

  case 168:

/* Line 1455 of yacc.c  */
#line 410 "parse.y"
    { chan->Seed = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 169:

/* Line 1455 of yacc.c  */
#line 413 "parse.y"
    { twoptr = chan->eHalfMinM; ;}
    break;

  case 171:

/* Line 1455 of yacc.c  */
#line 414 "parse.y"
    { twoptr = chan->tauScaleM; ;}
    break;

  case 173:

/* Line 1455 of yacc.c  */
#line 415 "parse.y"
    { chan->slopeM [0] = (yyvsp[(2) - (4)].rval);
                                            chan->slopeM [1] = (yyvsp[(3) - (4)].rval);
                                            chan->slopeM [2] = (yyvsp[(4) - (4)].rval); ;}
    break;

  case 174:

/* Line 1455 of yacc.c  */
#line 418 "parse.y"
    { chan->slopeM_stdev = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 175:

/* Line 1455 of yacc.c  */
#line 421 "parse.y"
    { twoptr = chan->CA_SCALE; ;}
    break;

  case 177:

/* Line 1455 of yacc.c  */
#line 422 "parse.y"
    { twoptr = chan->CA_EXP; ;}
    break;

  case 179:

/* Line 1455 of yacc.c  */
#line 423 "parse.y"
    { twoptr = chan->CA_EXP_RANGE; ;}
    break;

  case 181:

/* Line 1455 of yacc.c  */
#line 424 "parse.y"
    { twoptr = chan->CA_HALF_MIN; ;}
    break;

  case 183:

/* Line 1455 of yacc.c  */
#line 425 "parse.y"
    { twoptr = chan->CA_TAU_SCALE; ;}
    break;

  case 185:

/* Line 1455 of yacc.c  */
#line 428 "parse.y"
    { twoptr = chan->H_Initial; ;}
    break;

  case 187:

/* Line 1455 of yacc.c  */
#line 429 "parse.y"
    { twoptr = chan->hPower;    ;}
    break;

  case 189:

/* Line 1455 of yacc.c  */
#line 430 "parse.y"
    { twoptr = chan->eHalfMinM;  ;}
    break;

  case 191:

/* Line 1455 of yacc.c  */
#line 431 "parse.y"
    { twoptr = chan->eHalfMinH;  ;}
    break;

  case 193:

/* Line 1455 of yacc.c  */
#line 432 "parse.y"
    { chan->slopeM [0] = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 194:

/* Line 1455 of yacc.c  */
#line 433 "parse.y"
    { chan->slopeM_stdev = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 195:

/* Line 1455 of yacc.c  */
#line 434 "parse.y"
    { chan->slopeH [0] = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 196:

/* Line 1455 of yacc.c  */
#line 435 "parse.y"
    { chan->slopeH_stdev = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 197:

/* Line 1455 of yacc.c  */
#line 437 "parse.y"
    { chan->ValM_stdev  = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 198:

/* Line 1455 of yacc.c  */
#line 438 "parse.y"
    { chan->VoltM_stdev = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 199:

/* Line 1455 of yacc.c  */
#line 439 "parse.y"
    { chan->ValH_stdev  = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 200:

/* Line 1455 of yacc.c  */
#line 440 "parse.y"
    { chan->VoltH_stdev = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 201:

/* Line 1455 of yacc.c  */
#line 442 "parse.y"
    { nval = 0; ;}
    break;

  case 202:

/* Line 1455 of yacc.c  */
#line 442 "parse.y"
    { chan->nValM  = nval; chan->TauValM  = allocVlist (nval, vlist); ;}
    break;

  case 203:

/* Line 1455 of yacc.c  */
#line 443 "parse.y"
    { nval = 0; ;}
    break;

  case 204:

/* Line 1455 of yacc.c  */
#line 443 "parse.y"
    { chan->nVoltM = nval; chan->TauVoltM = allocVlist (nval, vlist); ;}
    break;

  case 205:

/* Line 1455 of yacc.c  */
#line 444 "parse.y"
    { nval = 0; ;}
    break;

  case 206:

/* Line 1455 of yacc.c  */
#line 444 "parse.y"
    { chan->nValH  = nval; chan->TauValH  = allocVlist (nval, vlist); ;}
    break;

  case 207:

/* Line 1455 of yacc.c  */
#line 445 "parse.y"
    { nval = 0; ;}
    break;

  case 208:

/* Line 1455 of yacc.c  */
#line 445 "parse.y"
    { chan->nVoltH = nval; chan->TauVoltH = allocVlist (nval, vlist); ;}
    break;

  case 209:

/* Line 1455 of yacc.c  */
#line 448 "parse.y"
    { twoptr = chan->eHalfMinM; ;}
    break;

  case 211:

/* Line 1455 of yacc.c  */
#line 449 "parse.y"
    { twoptr = chan->eHalfMinH;  ;}
    break;

  case 213:

/* Line 1455 of yacc.c  */
#line 450 "parse.y"
    { twoptr = chan->H_Initial; ;}
    break;

  case 215:

/* Line 1455 of yacc.c  */
#line 451 "parse.y"
    { twoptr = chan->hPower;    ;}
    break;

  case 217:

/* Line 1455 of yacc.c  */
#line 452 "parse.y"
    { twoptr = chan->tauScaleM; ;}
    break;

  case 219:

/* Line 1455 of yacc.c  */
#line 453 "parse.y"
    { twoptr = chan->tauScaleH; ;}
    break;

  case 221:

/* Line 1455 of yacc.c  */
#line 454 "parse.y"
    { chan->slopeM [0] = (yyvsp[(2) - (3)].rval);
                                      chan->slopeM [1] = (yyvsp[(3) - (3)].rval); ;}
    break;

  case 222:

/* Line 1455 of yacc.c  */
#line 456 "parse.y"
    { chan->slopeH [0] = (yyvsp[(2) - (3)].rval);
                                      chan->slopeH [1] = (yyvsp[(3) - (3)].rval); ;}
    break;

  case 223:

/* Line 1455 of yacc.c  */
#line 458 "parse.y"
    { chan->slopeM_stdev = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 224:

/* Line 1455 of yacc.c  */
#line 459 "parse.y"
    { chan->slopeH_stdev = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 225:

/* Line 1455 of yacc.c  */
#line 460 "parse.y"
    { twoptr = chan->alphaScaleFactorM; ;}
    break;

  case 227:

/* Line 1455 of yacc.c  */
#line 461 "parse.y"
    { twoptr = chan->betaScaleFactorM; ;}
    break;

  case 229:

/* Line 1455 of yacc.c  */
#line 462 "parse.y"
    { twoptr = chan->alphaScaleFactorH; ;}
    break;

  case 231:

/* Line 1455 of yacc.c  */
#line 463 "parse.y"
    { twoptr = chan->betaScaleFactorH; ;}
    break;

  case 233:

/* Line 1455 of yacc.c  */
#line 468 "parse.y"
    { syn = makesynapse (); ;}
    break;

  case 237:

/* Line 1455 of yacc.c  */
#line 475 "parse.y"
    { syn->L.name    = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 238:

/* Line 1455 of yacc.c  */
#line 476 "parse.y"
    { syn->Seed      = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 239:

/* Line 1455 of yacc.c  */
#line 477 "parse.y"
    { syn->SfdName   = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 240:

/* Line 1455 of yacc.c  */
#line 478 "parse.y"
    { syn->LearnName = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 241:

/* Line 1455 of yacc.c  */
#line 479 "parse.y"
    { syn->DataName  = strdup ((yyvsp[(2) - (2)].sval)); 
                                    deprecate (TK_DATA_LABEL); ;}
    break;

  case 242:

/* Line 1455 of yacc.c  */
#line 481 "parse.y"
    { syn->AugmentationName = strdup ( (yyvsp[(2) - (2)].sval) ); ;}
    break;

  case 243:

/* Line 1455 of yacc.c  */
#line 482 "parse.y"
    { syn->PsgName   = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 244:

/* Line 1455 of yacc.c  */
#line 483 "parse.y"
    { twoptr = syn->USE; ;}
    break;

  case 246:

/* Line 1455 of yacc.c  */
#line 484 "parse.y"
    { twoptr = syn->SynDelay; ;}
    break;

  case 248:

/* Line 1455 of yacc.c  */
#line 485 "parse.y"
    { twoptr = syn->SynRever; ;}
    break;

  case 250:

/* Line 1455 of yacc.c  */
#line 486 "parse.y"
    { twoptr = syn->MaxG; ;}
    break;

  case 252:

/* Line 1455 of yacc.c  */
#line 487 "parse.y"
    { twoptr = syn->InitRSE; ;}
    break;

  case 254:

/* Line 1455 of yacc.c  */
#line 488 "parse.y"
    { twoptr = syn->InitDeltaT; ;}
    break;

  case 256:

/* Line 1455 of yacc.c  */
#line 489 "parse.y"
    {
            if( syn->nToggles % 10 == 0 )  //need to allocate more space
            {
                syn->toggleTimes = (double*) realloc( syn->toggleTimes, sizeof(double)*(syn->nToggles+10) );
                syn->toggleModes = (int*) realloc( syn->toggleModes, sizeof(int)*(syn->nToggles+10) );
            }
            syn->toggleTimes[syn->nToggles] = (yyvsp[(2) - (2)].rval);
            syn->toggleModes[syn->nToggles++] = 1;
        ;}
    break;

  case 257:

/* Line 1455 of yacc.c  */
#line 498 "parse.y"
    {
            if( syn->nToggles % 10 == 0 )  //need to allocate more space
            {
                syn->toggleTimes = (double*) realloc( syn->toggleTimes, sizeof(double)*(syn->nToggles+10) );
                syn->toggleModes = (int*) realloc( syn->toggleModes, sizeof(int)*(syn->nToggles+10) );
            }
            syn->toggleTimes[syn->nToggles] = (yyvsp[(2) - (2)].rval);
            syn->toggleModes[syn->nToggles++] = 0;
        ;}
    break;

  case 258:

/* Line 1455 of yacc.c  */
#line 511 "parse.y"
    { syn_psg = makesyn_psg (); ;}
    break;

  case 262:

/* Line 1455 of yacc.c  */
#line 518 "parse.y"
    { syn_psg->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 263:

/* Line 1455 of yacc.c  */
#line 519 "parse.y"
    { syn_psg->File   = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 264:

/* Line 1455 of yacc.c  */
#line 524 "parse.y"
    { syn_fd = makesyn_fd (); ;}
    break;

  case 268:

/* Line 1455 of yacc.c  */
#line 531 "parse.y"
    { syn_fd->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 269:

/* Line 1455 of yacc.c  */
#line 532 "parse.y"
    { syn_fd->Seed   = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 270:

/* Line 1455 of yacc.c  */
#line 533 "parse.y"
    { syn_fd->SFD    = SFDCode ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 271:

/* Line 1455 of yacc.c  */
#line 534 "parse.y"
    { twoptr = syn_fd->Facil_Tau; ;}
    break;

  case 273:

/* Line 1455 of yacc.c  */
#line 535 "parse.y"
    { twoptr = syn_fd->Depr_Tau; ;}
    break;

  case 275:

/* Line 1455 of yacc.c  */
#line 540 "parse.y"
    { syn_learn = makesyn_learn (); ;}
    break;

  case 279:

/* Line 1455 of yacc.c  */
#line 547 "parse.y"
    { syn_learn->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 280:

/* Line 1455 of yacc.c  */
#line 548 "parse.y"
    { syn_learn->Seed = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 281:

/* Line 1455 of yacc.c  */
#line 549 "parse.y"
    { syn_learn->Learning = LearnCode ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 282:

/* Line 1455 of yacc.c  */
#line 550 "parse.y"
    { syn_learn->Learning_Shape = LearnShape ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 283:

/* Line 1455 of yacc.c  */
#line 551 "parse.y"
    { twoptr = syn_learn->DownWind; ;}
    break;

  case 285:

/* Line 1455 of yacc.c  */
#line 552 "parse.y"
    { twoptr = syn_learn->UpWind; ;}
    break;

  case 287:

/* Line 1455 of yacc.c  */
#line 553 "parse.y"
    { twoptr = syn_learn->Neg_Heb_Peak_Delta_Use; ;}
    break;

  case 289:

/* Line 1455 of yacc.c  */
#line 554 "parse.y"
    { twoptr = syn_learn->Pos_Heb_Peak_Delta_Use; ;}
    break;

  case 291:

/* Line 1455 of yacc.c  */
#line 555 "parse.y"
    { twoptr = syn_learn->Neg_Heb_Peak_Time; ;}
    break;

  case 293:

/* Line 1455 of yacc.c  */
#line 556 "parse.y"
    { twoptr = syn_learn->Pos_Heb_Peak_Time; ;}
    break;

  case 295:

/* Line 1455 of yacc.c  */
#line 561 "parse.y"
    { syn_data = makesyn_data (); 
                        deprecate (TK_SYN_DATA); ;}
    break;

  case 299:

/* Line 1455 of yacc.c  */
#line 569 "parse.y"
    { syn_data->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 300:

/* Line 1455 of yacc.c  */
#line 570 "parse.y"
    { syn_data->Seed   = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 301:

/* Line 1455 of yacc.c  */
#line 571 "parse.y"
    { twoptr = syn_data->MaxG; ;}
    break;

  case 303:

/* Line 1455 of yacc.c  */
#line 572 "parse.y"
    { twoptr = syn_data->SynDelay; ;}
    break;

  case 305:

/* Line 1455 of yacc.c  */
#line 573 "parse.y"
    { twoptr = syn_data->SynRever; ;}
    break;

  case 307:

/* Line 1455 of yacc.c  */
#line 578 "parse.y"
    { syn_augmentation = makesyn_augmentation (); ;}
    break;

  case 311:

/* Line 1455 of yacc.c  */
#line 584 "parse.y"
    { syn_augmentation->L.name = strdup ((yyvsp[(2) - (2)].sval) ); ;}
    break;

  case 312:

/* Line 1455 of yacc.c  */
#line 585 "parse.y"
    { twoptr = syn_augmentation->CA_init; ;}
    break;

  case 314:

/* Line 1455 of yacc.c  */
#line 586 "parse.y"
    { twoptr = syn_augmentation->CA_decay; ;}
    break;

  case 316:

/* Line 1455 of yacc.c  */
#line 587 "parse.y"
    { twoptr = syn_augmentation->CA_tau; ;}
    break;

  case 318:

/* Line 1455 of yacc.c  */
#line 588 "parse.y"
    { twoptr = syn_augmentation->CA_increment; ;}
    break;

  case 320:

/* Line 1455 of yacc.c  */
#line 589 "parse.y"
    { twoptr = syn_augmentation->MaxSA; ;}
    break;

  case 322:

/* Line 1455 of yacc.c  */
#line 590 "parse.y"
    { twoptr = syn_augmentation->Alpha; ;}
    break;

  case 324:

/* Line 1455 of yacc.c  */
#line 591 "parse.y"
    { twoptr = syn_augmentation->Augmentation_init; ;}
    break;

  case 326:

/* Line 1455 of yacc.c  */
#line 592 "parse.y"
    { twoptr = syn_augmentation->Augmentation_tau; ;}
    break;

  case 328:

/* Line 1455 of yacc.c  */
#line 593 "parse.y"
    { twoptr = syn_augmentation->SA_delay; ;}
    break;

  case 330:

/* Line 1455 of yacc.c  */
#line 598 "parse.y"
    { spike = makespike (); ;}
    break;

  case 334:

/* Line 1455 of yacc.c  */
#line 605 "parse.y"
    { spike->L.name = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 335:

/* Line 1455 of yacc.c  */
#line 606 "parse.y"
    { nval = 0; ;}
    break;

  case 336:

/* Line 1455 of yacc.c  */
#line 606 "parse.y"
    { spike->nVoltages = nval;
                                              spike->Voltages  = allocRVlist (nval, vlist); ;}
    break;

  case 337:

/* Line 1455 of yacc.c  */
#line 612 "parse.y"
    { stim = makestim (); ;}
    break;

  case 341:

/* Line 1455 of yacc.c  */
#line 619 "parse.y"
    { stim->L.name          = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 342:

/* Line 1455 of yacc.c  */
#line 620 "parse.y"
    { stim->MODE            = ModeCode ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 343:

/* Line 1455 of yacc.c  */
#line 621 "parse.y"
    { stim->PATTERN         = PatternCode ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 344:

/* Line 1455 of yacc.c  */
#line 622 "parse.y"
    { stim->VERT_TRANS      = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 345:

/* Line 1455 of yacc.c  */
#line 623 "parse.y"
    { stim->PHASE     = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 346:

/* Line 1455 of yacc.c  */
#line 624 "parse.y"
    { stim->Rate            = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 347:

/* Line 1455 of yacc.c  */
#line 625 "parse.y"
    { stim->Tau             = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 348:

/* Line 1455 of yacc.c  */
#line 626 "parse.y"
    { stim->Correl          = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 349:

/* Line 1455 of yacc.c  */
#line 627 "parse.y"
    { stim->TIMING          = TimingCode ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 350:

/* Line 1455 of yacc.c  */
#line 628 "parse.y"
    { stim->FileName        = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 351:

/* Line 1455 of yacc.c  */
#line 629 "parse.y"
    { stim->Port            = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 352:

/* Line 1455 of yacc.c  */
#line 630 "parse.y"
    { stim->Port            = -1; ;}
    break;

  case 353:

/* Line 1455 of yacc.c  */
#line 631 "parse.y"
    { stim->SAME_SEED       = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 354:

/* Line 1455 of yacc.c  */
#line 632 "parse.y"
    { stim->Seed            = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 355:

/* Line 1455 of yacc.c  */
#line 633 "parse.y"
    { stim->nFreqs          = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 356:

/* Line 1455 of yacc.c  */
#line 634 "parse.y"
    { stim->CellsPerFreq    = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 357:

/* Line 1455 of yacc.c  */
#line 635 "parse.y"
    { twoptr = stim->Time_Freq_Incr; ;}
    break;

  case 359:

/* Line 1455 of yacc.c  */
#line 636 "parse.y"
    { twoptr = stim->DynRange; ;}
    break;

  case 361:

/* Line 1455 of yacc.c  */
#line 637 "parse.y"
    { stim->AMP_Start       = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 362:

/* Line 1455 of yacc.c  */
#line 638 "parse.y"
    { stim->AMP_End         = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 363:

/* Line 1455 of yacc.c  */
#line 639 "parse.y"
    { stim->WidthSec        = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 364:

/* Line 1455 of yacc.c  */
#line 640 "parse.y"
    { stim->FREQ_Start      = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 365:

/* Line 1455 of yacc.c  */
#line 641 "parse.y"
    { nval = 0; ;}
    break;

  case 366:

/* Line 1455 of yacc.c  */
#line 641 "parse.y"
    { stim->nTStart = nval; 
                                            stim->TStart  = allocVlist (nval, vlist); ;}
    break;

  case 367:

/* Line 1455 of yacc.c  */
#line 643 "parse.y"
    { nval = 0; ;}
    break;

  case 368:

/* Line 1455 of yacc.c  */
#line 643 "parse.y"
    { stim->nTStop  = nval;
                                            stim->TStop   = allocVlist (nval, vlist); ;}
    break;

  case 369:

/* Line 1455 of yacc.c  */
#line 649 "parse.y"
    { sti = makesti (); ;}
    break;

  case 373:

/* Line 1455 of yacc.c  */
#line 656 "parse.y"
    { sti->L.name      = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 374:

/* Line 1455 of yacc.c  */
#line 657 "parse.y"
    { sti->StimName    = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 375:

/* Line 1455 of yacc.c  */
#line 659 "parse.y"
    { sti->ColName  = strdup ((yyvsp[(2) - (6)].sval));
                            sti->LayName  = strdup ((yyvsp[(3) - (6)].sval));
                            sti->CellName = strdup ((yyvsp[(4) - (6)].sval));
                            sti->CmpName  = strdup ((yyvsp[(5) - (6)].sval));
                            sti->Prob     = (yyvsp[(6) - (6)].rval); ;}
    break;

  case 376:

/* Line 1455 of yacc.c  */
#line 668 "parse.y"
    { report = makereport (); ;}
    break;

  case 380:

/* Line 1455 of yacc.c  */
#line 675 "parse.y"
    { report->L.name    = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 381:

/* Line 1455 of yacc.c  */
#line 677 "parse.y"
    { report->ColName   = strdup ((yyvsp[(2) - (5)].sval));
                                   report->LayName   = strdup ((yyvsp[(3) - (5)].sval));
                                   report->CellName  = strdup ((yyvsp[(4) - (5)].sval));
                                   report->CmpName   = strdup ((yyvsp[(5) - (5)].sval)); ;}
    break;

  case 382:

/* Line 1455 of yacc.c  */
#line 681 "parse.y"
    { report->FileName  = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 383:

/* Line 1455 of yacc.c  */
#line 682 "parse.y"
    { report->Port      = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 384:

/* Line 1455 of yacc.c  */
#line 683 "parse.y"
    { report->Port      = -1; ;}
    break;

  case 385:

/* Line 1455 of yacc.c  */
#line 684 "parse.y"
    { report->ASCII     = TRUE; ;}
    break;

  case 386:

/* Line 1455 of yacc.c  */
#line 685 "parse.y"
    { report->reportFlag |= 1;
                                   report->ASCII     = TRUE; ;}
    break;

  case 387:

/* Line 1455 of yacc.c  */
#line 687 "parse.y"
    { report->ReportOn  = ReportCode ("CHANNEL_RPT");
                                   report->Name      = strdup ((yyvsp[(2) - (2)].sval)); 
                                   printf ("Report Channel: code = %x, name = '%s'\n", report->ReportOn, report->Name); ;}
    break;

  case 388:

/* Line 1455 of yacc.c  */
#line 690 "parse.y"
    { report->ReportOn  = ReportCode ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 389:

/* Line 1455 of yacc.c  */
#line 691 "parse.y"
    { report->CellSequence = CellSequenceCode ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 390:

/* Line 1455 of yacc.c  */
#line 692 "parse.y"
    { report->Prob      = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 391:

/* Line 1455 of yacc.c  */
#line 693 "parse.y"
    { report->Frequency = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 392:

/* Line 1455 of yacc.c  */
#line 694 "parse.y"
    { nval = 0; ;}
    break;

  case 393:

/* Line 1455 of yacc.c  */
#line 695 "parse.y"
    { report->nTStart = nval;
                                   report->TStart  = allocVlist (nval, vlist); ;}
    break;

  case 394:

/* Line 1455 of yacc.c  */
#line 697 "parse.y"
    { nval = 0; ;}
    break;

  case 395:

/* Line 1455 of yacc.c  */
#line 698 "parse.y"
    { report->nTStop  = nval;
                                   report->TStop   = allocVlist (nval, vlist); ;}
    break;

  case 396:

/* Line 1455 of yacc.c  */
#line 700 "parse.y"
    { report->ReportOn = ReportCode ("SYNAPSE_USE");
                                   report->Name     = strdup ((yyvsp[(2) - (2)].sval)); ;}
    break;

  case 397:

/* Line 1455 of yacc.c  */
#line 702 "parse.y"
    {
                                   report->ReportOn = ReportCode ("SYNAPSE_RSE");
                                   report->Name     = strdup ((yyvsp[(2) - (2)].sval));
                                 ;}
    break;

  case 398:

/* Line 1455 of yacc.c  */
#line 706 "parse.y"
    {
                                   report->ReportOn = ReportCode ("SYNAPSE_UF");
                                   report->Name     = strdup ((yyvsp[(2) - (2)].sval));
                                 ;}
    break;

  case 399:

/* Line 1455 of yacc.c  */
#line 710 "parse.y"
    {
                                       report->ReportOn = ReportCode ("SYNAPSE_SA");
                                       report->Name     = strdup ((yyvsp[(2) - (2)].sval));
                                     ;}
    break;

  case 400:

/* Line 1455 of yacc.c  */
#line 714 "parse.y"
    {
                                       report->ReportOn = ReportCode ("SYNAPSE_CA");
                                       report->Name     = strdup ((yyvsp[(2) - (2)].sval));
                                     ;}
    break;

  case 401:

/* Line 1455 of yacc.c  */
#line 718 "parse.y"
    { report->Seed = (yyvsp[(2) - (2)].ival); ;}
    break;

  case 402:

/* Line 1455 of yacc.c  */
#line 719 "parse.y"
    { report->Seed = SELECT_FRONT; ;}
    break;

  case 403:

/* Line 1455 of yacc.c  */
#line 720 "parse.y"
    { report->reportFlag |= (yyvsp[(2) - (2)].ival); ;}
    break;

  case 404:

/* Line 1455 of yacc.c  */
#line 721 "parse.y"
    { ;}
    break;

  case 405:

/* Line 1455 of yacc.c  */
#line 724 "parse.y"
    { event = makeevent(); ;}
    break;

  case 409:

/* Line 1455 of yacc.c  */
#line 731 "parse.y"
    { event->L.name = strdup( (yyvsp[(2) - (2)].sval) ); ;}
    break;

  case 410:

/* Line 1455 of yacc.c  */
#line 732 "parse.y"
    { event->synapseName = strdup( (yyvsp[(2) - (2)].sval) ); ;}
    break;

  case 411:

/* Line 1455 of yacc.c  */
#line 733 "parse.y"
    { 
            event->cellGroupNames[0] = strdup( (yyvsp[(2) - (5)].sval) );
            event->cellGroupNames[1] = strdup( (yyvsp[(3) - (5)].sval) );
            event->cellGroupNames[2] = strdup( (yyvsp[(4) - (5)].sval) );
            event->cellGroupNames[3] = strdup( (yyvsp[(5) - (5)].sval) );
        ;}
    break;

  case 412:

/* Line 1455 of yacc.c  */
#line 739 "parse.y"
    { event->file = strdup( (yyvsp[(2) - (3)].sval) ); event->time = (yyvsp[(3) - (3)].rval); ;}
    break;

  case 415:

/* Line 1455 of yacc.c  */
#line 747 "parse.y"
    { report->reportFlag |= AVERAGE_SYN; ;}
    break;

  case 416:

/* Line 1455 of yacc.c  */
#line 748 "parse.y"
    { report->reportFlag |= HIDE_STEP; ;}
    break;

  case 417:

/* Line 1455 of yacc.c  */
#line 753 "parse.y"
    { if (nval < VSIZE) vlist [nval++] = (yyvsp[(1) - (1)].rval); ;}
    break;

  case 418:

/* Line 1455 of yacc.c  */
#line 754 "parse.y"
    { if (nval < VSIZE) vlist [nval++] = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 419:

/* Line 1455 of yacc.c  */
#line 757 "parse.y"
    { twoptr [0] = (yyvsp[(1) - (2)].rval); twoptr [1] = (yyvsp[(2) - (2)].rval); ;}
    break;

  case 420:

/* Line 1455 of yacc.c  */
#line 758 "parse.y"
    { twoptr [0] = (yyvsp[(1) - (1)].rval); twoptr [1] = 0.0; ;}
    break;

  case 421:

/* Line 1455 of yacc.c  */
#line 761 "parse.y"
    { (yyval.rval) = (double) (yyvsp[(1) - (1)].ival); ;}
    break;

  case 422:

/* Line 1455 of yacc.c  */
#line 762 "parse.y"
    { (yyval.rval) = (yyvsp[(1) - (1)].rval); ;}
    break;



/* Line 1455 of yacc.c  */
#line 4376 "parse.c"
      default: break;
    }
  YY_SYMBOL_PRINT ("-> $$ =", yyr1[yyn], &yyval, &yyloc);

  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);

  *++yyvsp = yyval;

  /* Now `shift' the result of the reduction.  Determine what state
     that goes to, based on the state we popped back to and the rule
     number reduced by.  */

  yyn = yyr1[yyn];

  yystate = yypgoto[yyn - YYNTOKENS] + *yyssp;
  if (0 <= yystate && yystate <= YYLAST && yycheck[yystate] == *yyssp)
    yystate = yytable[yystate];
  else
    yystate = yydefgoto[yyn - YYNTOKENS];

  goto yynewstate;


/*------------------------------------.
| yyerrlab -- here on detecting error |
`------------------------------------*/
yyerrlab:
  /* If not already recovering from an error, report this error.  */
  if (!yyerrstatus)
    {
      ++yynerrs;
#if ! YYERROR_VERBOSE
      yyerror (YY_("syntax error"));
#else
      {
	YYSIZE_T yysize = yysyntax_error (0, yystate, yychar);
	if (yymsg_alloc < yysize && yymsg_alloc < YYSTACK_ALLOC_MAXIMUM)
	  {
	    YYSIZE_T yyalloc = 2 * yysize;
	    if (! (yysize <= yyalloc && yyalloc <= YYSTACK_ALLOC_MAXIMUM))
	      yyalloc = YYSTACK_ALLOC_MAXIMUM;
	    if (yymsg != yymsgbuf)
	      YYSTACK_FREE (yymsg);
	    yymsg = (char *) YYSTACK_ALLOC (yyalloc);
	    if (yymsg)
	      yymsg_alloc = yyalloc;
	    else
	      {
		yymsg = yymsgbuf;
		yymsg_alloc = sizeof yymsgbuf;
	      }
	  }

	if (0 < yysize && yysize <= yymsg_alloc)
	  {
	    (void) yysyntax_error (yymsg, yystate, yychar);
	    yyerror (yymsg);
	  }
	else
	  {
	    yyerror (YY_("syntax error"));
	    if (yysize != 0)
	      goto yyexhaustedlab;
	  }
      }
#endif
    }



  if (yyerrstatus == 3)
    {
      /* If just tried and failed to reuse lookahead token after an
	 error, discard it.  */

      if (yychar <= YYEOF)
	{
	  /* Return failure if at end of input.  */
	  if (yychar == YYEOF)
	    YYABORT;
	}
      else
	{
	  yydestruct ("Error: discarding",
		      yytoken, &yylval);
	  yychar = YYEMPTY;
	}
    }

  /* Else will try to reuse lookahead token after shifting the error
     token.  */
  goto yyerrlab1;


/*---------------------------------------------------.
| yyerrorlab -- error raised explicitly by YYERROR.  |
`---------------------------------------------------*/
yyerrorlab:

  /* Pacify compilers like GCC when the user code never invokes
     YYERROR and the label yyerrorlab therefore never appears in user
     code.  */
  if (/*CONSTCOND*/ 0)
     goto yyerrorlab;

  /* Do not reclaim the symbols of the rule which action triggered
     this YYERROR.  */
  YYPOPSTACK (yylen);
  yylen = 0;
  YY_STACK_PRINT (yyss, yyssp);
  yystate = *yyssp;
  goto yyerrlab1;


/*-------------------------------------------------------------.
| yyerrlab1 -- common code for both syntax error and YYERROR.  |
`-------------------------------------------------------------*/
yyerrlab1:
  yyerrstatus = 3;	/* Each real token shifted decrements this.  */

  for (;;)
    {
      yyn = yypact[yystate];
      if (yyn != YYPACT_NINF)
	{
	  yyn += YYTERROR;
	  if (0 <= yyn && yyn <= YYLAST && yycheck[yyn] == YYTERROR)
	    {
	      yyn = yytable[yyn];
	      if (0 < yyn)
		break;
	    }
	}

      /* Pop the current state because it cannot handle the error token.  */
      if (yyssp == yyss)
	YYABORT;


      yydestruct ("Error: popping",
		  yystos[yystate], yyvsp);
      YYPOPSTACK (1);
      yystate = *yyssp;
      YY_STACK_PRINT (yyss, yyssp);
    }

  *++yyvsp = yylval;


  /* Shift the error token.  */
  YY_SYMBOL_PRINT ("Shifting", yystos[yyn], yyvsp, yylsp);

  yystate = yyn;
  goto yynewstate;


/*-------------------------------------.
| yyacceptlab -- YYACCEPT comes here.  |
`-------------------------------------*/
yyacceptlab:
  yyresult = 0;
  goto yyreturn;

/*-----------------------------------.
| yyabortlab -- YYABORT comes here.  |
`-----------------------------------*/
yyabortlab:
  yyresult = 1;
  goto yyreturn;

#if !defined(yyoverflow) || YYERROR_VERBOSE
/*-------------------------------------------------.
| yyexhaustedlab -- memory exhaustion comes here.  |
`-------------------------------------------------*/
yyexhaustedlab:
  yyerror (YY_("memory exhausted"));
  yyresult = 2;
  /* Fall through.  */
#endif

yyreturn:
  if (yychar != YYEMPTY)
     yydestruct ("Cleanup: discarding lookahead",
		 yytoken, &yylval);
  /* Do not reclaim the symbols of the rule which action triggered
     this YYABORT or YYACCEPT.  */
  YYPOPSTACK (yylen);
  YY_STACK_PRINT (yyss, yyssp);
  while (yyssp != yyss)
    {
      yydestruct ("Cleanup: popping",
		  yystos[*yyssp], yyvsp);
      YYPOPSTACK (1);
    }
#ifndef yyoverflow
  if (yyss != yyssa)
    YYSTACK_FREE (yyss);
#endif
#if YYERROR_VERBOSE
  if (yymsg != yymsgbuf)
    YYSTACK_FREE (yymsg);
#endif
  /* Make sure YYID is used.  */
  return YYID (yyresult);
}



/* Line 1675 of yacc.c  */
#line 765 "parse.y"


int multiInput( char *fname )
{
  INFILE latest;

  if( !initFlag )  //is this the first time we're including another input file?
  {
    initFileStack( &fileStack );
    initFlag = 1;
  }

  latest.from = NULL;
  latest.file = strdup( fname );//filename to be opened
  latest.parentFile = strdup( currentFile );
  latest.line = TIN->line;//remember where in the current input file this was included
  latest.col = 0;

  pushFileStack( &fileStack, &latest );

  if( latest.file ) free( latest.file );
}

int yywrap(void)
{
  INFILE *next = NULL;
  struct stat fs;
  int nbytes;
  FILE *in;

  if( initFlag )
  {
    next = popFileStack( &fileStack, next );
    while( next != NULL )
    {
      //bring in new info

      stat( next->file, &fs );
      nbytes = fs.st_size;
      in = fopen( next->file, "r" );

      if( !in )
      {
        fprintf( stderr, "Error: could not open file %s\n", next->file );
        fprintf( stderr, "\tdefined in file %s, line %d\n", next->parentFile, next->line );

        printf( "Error: could not open file %s\n", next->file );
        printf( "\tdefined in file %s, line %d\n", next->parentFile, next->line );

        free( next->parentFile );
        free( next->file );
        free( next );
        next = popFileStack( &fileStack, next );
        continue;
      }

      free( currentFile );
      currentFile = strdup( next->file );
      TIN->line = 0;
      yy_switch_to_buffer( yy_create_buffer( in, fs.st_size ) );  //should I store the return value somewhere?

      //these lines make it break, but why? I need to deallocate this memory, don't I?
      //free( next->parentFile );
      //free( next->file );
      //free( next );

      return 0;  //continue parsing
    }

    //next == NULL if I get here, so the fileStack is empty
    destroyFileStack( &fileStack );
    return 1;  //end parsing
  } 
  
  return 1;  //end parsing
}

yyerror (char *str)
{
  printerr ("%s:%d: %s\n", TIN->file, TIN->line, str);
  TIN->nParseErr++;
}

unused (int kind)
{
  printerr ("%s:%d: Warning: Keyword '%s' no longer used\n",
            TIN->file, TIN->line, TK2name (kind));
}

deprecate (int kind)
{
//printerr ("%s:%d: Warning: Keyword '%s' is deprecated\n",
//          TIN->file, TIN->line, TK2name (kind));
}

/*-----------------------------------------------------------------------

This is the parser for ncs input files.  It accepts tokens from the lexical
analyzer (scan.l).  Tokens may be known keywords (as listed in the %tokens)
section, or variables, which can be INTEGER, REAL, LOGICAL, or STRING.  The
parser creates input structures and assigns values to them according to the
rules of the input language.

The format for most brain elements is the same: the parser sees the token
for an element, creates a structure for that element (entering it into the
list of structures), then recognizes keyword-value sets allowed for that
element and assigns the values to the structure elements.


TODO:

  Need more informative error messages for parse errors.

  Add INCLUDE file capability.

  Someone who knows more about YACC/Bison might be able to improve on this
  set of grammar rules.
-----------------------------------------------------------------------*/

