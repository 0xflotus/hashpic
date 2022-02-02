# Hashpic

Hashpic creates an image from the MD5 hash of your input.

### Install

`pip3 install hashpic`

### Usage

```bash
> python3 -m hashpic 'Hashpic rocks!'
```

This should create a file `output.png` in your current directory. 
The input `Hashpic rocks!` should create the following image:

![hashpic image](./docs/rocks.png)

#### Disclaimer

The color palette in `data.py` was copied and influenced from the [`string-color`](https://pypi.org/project/string-color/) library. 
Thanks for this!
