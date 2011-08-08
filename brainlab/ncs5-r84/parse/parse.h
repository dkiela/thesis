
/* A Bison parser, made by GNU Bison 2.4.1.  */

/* Skeleton interface for Bison's Yacc-like parsers in C
   
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

/* Line 1676 of yacc.c  */
#line 51 "parse.y"

  double rval;
  int    ival;
  char   sval [STRLEN];



/* Line 1676 of yacc.c  */
#line 257 "parse.h"
} YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define yystype YYSTYPE /* obsolescent; will be withdrawn */
# define YYSTYPE_IS_DECLARED 1
#endif

extern YYSTYPE yylval;


