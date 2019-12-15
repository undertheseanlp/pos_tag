# Gán nhãn từ loại tiếng Việt

![](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg)
![](https://img.shields.io/badge/opensource-vietnamese-blue.svg)
![](https://img.shields.io/badge/contributions-welcome-green.svg)

Dự án nghiên cứu về bài toán *gán nhãn từ loại tiếng Việt*, được phát triển bởi nhóm nghiên cứu xử lý ngôn ngữ tự nhiên tiếng Việt - [underthesea](https://github.com/undertheseanlp). Chứa mã nguồn các thử nghiệm cho việc xử lý dữ liệu, huấn luyện và đánh giá mô hình, cũng như cho phép dễ dàng tùy chỉnh mô hình đối với những tập dữ liệu mới.

**Nhóm tác giả** 

* Vũ Anh ([anhv.ict91@gmail.com](anhv.ict91@gmail.com))
* Bùi Nhật Anh ([buinhatanh1208@gmail.com](buinhatanh1208@gmail.com))

**Tham gia đóng góp**

Mọi ý kiến đóng góp hoặc yêu cầu trợ giúp xin gửi vào mục [Issues](../../issues) của dự án. Các thảo luận được khuyến khích **sử dụng tiếng Việt** để dễ dàng trong quá trình trao đổi. 

## 1. Installation

### 1.1 Requirements

* `Operating Systems: Linux (Ubuntu, CentOS), Mac`
* `Python 3.6`
* `Anaconda`
* `underthesea==1.1.9a2`

### 1.2 Download and Setup Environment

Clone project using git

```
$ git clone https://github.com/undertheseanlp/pos_tag.git
```

Create environment and install requirements

```
$ cd pos_tag
$ conda create -n pos_tag python=3.6
$ pip install -r requirements.txt
```

## 2. Usage

Make sure you are in `pos_tag` folder and activate `pos_tag` environment

```
$ cd pos_tag
$ source activate pos_tag
``` 

### 2.1 Using a pre-trained model

```
$ python pos_tag.py --text "Chàng trai 9X Quảng Trị khởi nghiệp từ nấm sò"
Chàng/Nc trai/N 9X/N Quảng_Trị/Np khởi_nghiệp/V từ/E nấm/N sò/M

$ python pos_tag.py --fin tmp/input.txt --fout tmp/output.txt
```

### 2.2 Train a new dataset

**Train and test**

```
$ python util/preprocess_vlsp2013.py
$ python train.py train-test \
    --train tmp/vlsp2013/train.txt \
    --test tmp/vlsp2013/test.txt
```

**Train and export model**

```
$ python train.py \
    --train tmp/vlsp2013/train.txt \
    --model tmp/model.bin
```

Predict with trained model

```
$ python pos_tag.py \
    --fin tmp/input.txt --fout tmp/output.txt \
    --model tmp/model.bin
```

## Bản quyền

Mã nguồn của dự án được phân phối theo giấy phép [GPL-3.0](LICENSE.txt).
