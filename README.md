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

#### Console Mode

<img width="1288" alt="Bildschirmfoto 2022-02-02 um 13 15 08" src="https://user-images.githubusercontent.com/26602940/152152075-d76d66d4-0ff0-4a75-a622-3bd6febcc52f.png">

### Disclaimer

The color palette in `data.py` was copied and influenced from the [`string-color`](https://pypi.org/project/string-color/) library. 
Thanks for this!
