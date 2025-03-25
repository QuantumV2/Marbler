<pre>
o - ball. The main instruction pointer starting position. Has gravity
# - floor/wall
0-9 - push the number onto the stack
+ - add numbers
- - subtract numbers
* - multiply
: - divide
% - modulo
$ - pop value and discard it
= - push 1 if numbers are equal , otherwise 0
r - reverse stack
s - swap two top stack values
d - duplicate top value on stack
b - push stack size onto the stack
& - pop data from stack and put it in the ball
~ - push data from the ball back onto the stack
/ - roll left if touched
\ - roll right if touched
], [ - springs, reverse ball direction if its rolling into the solid side
A - sucks the ball upwards if it doesnt have a value/the value is 0 inside of it (the ball is light), or else doesnt suck(the ball is too heavy)
_ , |, ^, v, >, < - pipe system, ball moves through it completely disregarding gravity, ball enters when it encounters a pipe character ,ball exits as soon as there is no pipe character
" - pop value from stack and print as a character 
` - pop value from stack and print as a number
. - input number
, - input string (pushes in reverse)
! - jump over the next command if light,  do not jump over if heavy


Ball falling out of the program - program end
<pre>
