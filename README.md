# Hashpic

Hashpic creates an image from the *MD5* hash of your input.

Since _v0.2.0_ it is also possible to create an image from a *SHA-512* hash.

Since _v0.2.3_ it is also possible to create an image from a *SHAKE-256* hash with variable digest length of _16_ or _64_.

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
> printf 'Hashpic rocks!' | md5 | python3 -m hashpic --md5

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

### Disclaimer

The color palette in `data.py` was copied and influenced from the [`string-color`](https://pypi.org/project/string-color/) library. 
Thanks for this!
