# 崩坏星穹铁道3.2版本活动星铁WORLD自动刷金币

## 前言

最近的新的版本活动发现好友卷的很，于是突发奇想安排了该脚本。试了一下刷了一上午已经刷到好友榜一（14.4HH）了。

~~可以挑战一下刷到ZZ级了，刚才发现作者已经被前榜一好友删掉了~~

## 功能

- 云游戏的支持(非常感谢@Nanboom233)
- 自动完成帕姆快送
- 自动来宾事件
- 自动薅鸟毛（
- 特殊来宾(非常感谢@SUC-DriverOld)
- 展览日结束后自动开始下一展览日
- 抽卡&角色升级 (非常感谢@SUC-DriverOld)

注：没有设计收金币功能，因为感觉意义不大，但是在完成帕姆配送时有概率误触导致金币被收

## 使用方法

在下图界面打开main.exe即可(推荐) 注：本程序需要管理员权限（否则无法在游戏全屏下模拟鼠标点击事件）（win10用户右键选择以管理员身份运行即可，11应该类似）
![img_1.png](mdimg/img_1.png)

或者下载源码执行
```bash
pip install -r requirements.txt
# 同样需要管理员权限
python main.py

# 更多命令行参数：
options:
  -h, --help            show this help message and exit
  --debug               debug模式
  --timer-seconds TIMER_SECONDS
                        定时器时间，默认3600秒（1小时）
  --disable-glod        禁止自动抽取贵金邀约
  --disable-common      禁止自动抽取标准邀约
  --disable-color       禁止自动抽取标准邀约
  --disable-use-diamonds
                        禁止使用钻石抽取
  --cloudgame           使用云游戏
```

(注：目前仅支持Windows全屏窗口)
![img.png](mdimg/img.png)

## 引个流(

演示视频：<a href = "https://www.bilibili.com/video/BV13vonYfEwx/">https://www.bilibili.com/video/BV13vonYfEwx/

有问题可以去评论区或者私信我，Issues不一定能及时回。
