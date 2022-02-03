# Hashpic

Hashpic creates an image from the *MD5* hash of your input.

Since _v0.2.0_ it is also possible to create an image from a *SHA-512* hash.

Since _v0.2.8_ it is also possible to create an image from a *SHAKE-256* hash with variable digest length of _16_, _25_, _36_ or _64_.

### Install

`pip3 install hashpic`

### Usage

```bash
> python3 -m hashpic 'Hashpic rocks!'
```

This should create a file `output.png` in your current directory. 
The input `Hashpic rocks!` should create the following image:

![hashpic image](./docs/rocks.png)

#### Piping from another program

All this commands should produce the same image as above.

```bash
> printf 'Hashpic rocks!' | md5 | python3 -m hashpic --bypass

> printf 'Hashpic rocks!' | python3 -m hashpic
```

#### Console Mode

![console](./docs/console.png)

#### SHA-512 Mode

It is also possible to create an image from a *SHA-512* hash. All arguments for *MD5 Mode* are also available for *SHA512 Mode*.

```bash
> python3 -m hashpic --sha512 'Hashpic rocks!'

> printf 'Hashpic rocks!' | python3 -m hashpic --sha512
```

This commands should create the following image:

![sha512 image](./docs/rocks_on_sha512.png)

### Examples

Bypassing a hash directly:

```bash
> python3 -m hashpic ff00ff00ff00ff0000ff00ff00ff00ffff00ff00ff00ff0000ff00ff00ff00ffff00ff00ff00ff0000ff00ff00ff00ffff00ff00ff00ff0000ff00ff00ff00ff --bypass --sha512
```

This command will produce the following image:

![bypassed](./docs/bypassed.png)

So we can call the hash above the so called `chessboard hash`.

You can also bypass a hash from another program:

```bash
> printf 'Hashpic rocks!' | sha512sum | awk '{print $1}' | python3 -m hashpic -c --sha512 --bypass
a11a61ccfce80f61
3aa90205a54afc67
e3b5fb495a4dfa29
e1c4171c8bf966a7
cfa50865bbd1004f
d2dc02015943010d
04c5db7df09d91ee
1a9172c68844b84c
```

### Disclaimer

The color palette in `data.py` was copied from and influenced by the [`string-color`](https://pypi.org/project/string-color/) library. 
Thanks for this!
