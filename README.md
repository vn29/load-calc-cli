# load-calc-cli
A simple python CLI for managing quick load calculations.
load-calc is a concept CLI tool written in less than 100 lines of python and with no 3rd party dependencies.
I wrote it in a few hours as a Proof-of-Concept. 
My goal was to make a simple tool for common quick calculations done typically by structural engineers while they are
computing load combinations over tributary widths and areas. I've always felt there was something I could create that was somewhere in-between using excel or mathcad and a calculator.
load-calc is my attempt at creating this.

## how to run
The script is extremely simple. If you have python 3 on your machine, simply run the script from the command line with `py load_calc_cli.py`.

## Examples
Load-calc is intelligent about how loads come together. You simply enter a two letter appreviation of the load type followed by the load and load-calc-cli will record it.
It will echo the current state of your load types you have entered.

```
MyLC Version 1.0.0 Command line tool for rapid load combination maniputations
>>DL 22k

DL 22k

>>LL 15k

DL 22k
LL 15k
```
Then, typing `LC:` followed by the load combination as shown will automatically gather the load types and sum them. you can enter any values here as long as they follow the convention
of a signed float followed by two alphabetical characters.
```

>>LC: 1.2DL 1.6LL

ultimate: 50.4
```
Starting a new example:
Loads can be stored with different units and the trib taken over. The arrow indicates multiplication over the trib resulting in final units of kip (k).

```
>>DL 5k/ft -> 10ft

DL 5k/ft -> 10ft

>>LL 10sqft -> 5ft -> 5ft

DL 5k/ft -> 10ft
LL 10sqft -> 5ft -> 5ft
```
Typing `s` will "shrink" the loads to their base.
```
>>s

DL 50.0
LL 250.0
```
And computing the LC we get

```
>>LC: 1.2DL -0.5LL 

ultimate: -65.0
```

We can even add additional loads to a specific load type by using the `+` symbol. Below is an example. Also, the -1 symbol after the `ft` in this example tell load-calc to divide
```
>>+DL 5ksf -> 10ft-1 -> 10ft-1

DL 5k/ft -> 10ft
LL 10sqft -> 5ft -> 5ft
+DL 5ksf -> 10ft-1 -> 10ft-1

>>LC: 1.2DL 1.6LL

ultimate: 460.06

```
and we can simply see the summarized per load type with the `s` command if we wish at any time.
```
>>s

DL 50.05
LL 250.0
```

Annotations can be added to the loads so you can keep track of what they are. First, we will overwrite our existing load type. re-entering it will overwrite.
 
```
>>DL self_weight:5k/ft -> beam_length:10ft 

DL self_weight:5k/ft -> beam_length:10ft
LL 10sqft -> 5ft -> 5ft
+DL 5ksf -> 10ft-1 -> 10ft-1
```
Lets add an annotated super imposed dead load
```
>>SD super_imposed:0.5k/ft -> beam_length:10ft

DL self_weight:5k/ft -> beam_length:10ft
LL 10sqft -> 5ft -> 5ft
+DL 5ksf -> 10ft-1 -> 10ft-1
SD super_imposed:0.5k/ft -> beam_length:10ft
```
Then we show how adding two plus sympbols allows for another distinguished load type `++` 
```
>>++DL extra:0.5k

DL self_weight:5k/ft -> beam_length:10ft
LL 10sqft -> 5ft -> 5ft
+DL 5ksf -> 10ft-1 -> 10ft-1
SD super_imposed:0.5k/ft -> beam_length:10ft
++DL extra:0.5k
```
And we can still use `s` as well as get our values for an `LC`.
```
>>s

DL 50.55
LL 250.0
SD 5.0

>>LC: 1.4DL 1.4SD

ultimate: 77.77
```

There are no restrictions on what you put for the units but you will need to track dimensional analysis. Here we show unit conversions to maintain results as k (kip).
```
>>WL 14lbf/sqft -> 10sqft -> 1000lbf/kip-1

DL self_weight:5k/ft -> beam_length:10ft
LL 10sqft -> 5ft -> 5ft
+DL 5ksf -> 10ft-1 -> 10ft-1
SD super_imposed:0.5k/ft -> beam_length:10ft
++DL extra:0.5k
WL 14lbf/sqft -> 10sqft -> 1000lbf/kip-1

>>s

DL 50.55
LL 250.0
SD 5.0
WL 0.14
```

to undo a load type, use `rm:` followed by the load type symbol (++DL here) (Also note here pressing enter with no imput will simpy echo the load types stored)

```
>>       

DL self_weight:5k/ft -> beam_length:10ft
SD super_imposed:0.5k/ft -> beam_length:10ft
+DL 5ksf -> 10ft-1 -> 10ft-1
WL 14lbf/sqft -> 10sqft -> 1000lbf/kip-1
LL 10sqft -> 5ft -> 5ft
++DL extra:0.5k

>>rm:++DL
>>

DL self_weight:5k/ft -> beam_length:10ft
SD super_imposed:0.5k/ft -> beam_length:10ft
+DL 5ksf -> 10ft-1 -> 10ft-1
WL 14lbf/sqft -> 10sqft -> 1000lbf/kip-1
LL 10sqft -> 5ft -> 5ft
```

`stored:<name>` will store the load types for the session under that name and can be recoverd with `recall:<name>`

`d` will delete the whole load type currently being worked on (it clears the terminal).

