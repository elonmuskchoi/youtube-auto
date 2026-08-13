import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H, FPS = 1280, 720, 24
CONTENT_H = 610
FONT_PATH = r"C:\Windows\Fonts\NotoSansKR-VF.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_PATH, size)


def fit(image, box):
    x0, y0, x1, y1 = box
    scale = min((x1-x0)/image.width, (y1-y0)/image.height)
    im = image.resize((int(image.width*scale), int(image.height*scale)), Image.Resampling.LANCZOS)
    return im, (x0+(x1-x0-im.width)//2, y0+(y1-y0-im.height)//2)


def captions(words):
    cues, current = [], []
    for word in words:
        candidate = " ".join(item["text"] for item in current + [word]).strip()
        duration = word["end"] - (current[0]["start"] if current else word["start"])
        if current and (len(candidate) > 24 or duration > 2.5):
            cues.append((current[0]["start"], current[-1]["end"] + .08, " ".join(x["text"] for x in current)))
            current = []
        current.append(word)
    if current:
        cues.append((current[0]["start"], current[-1]["end"] + .08, " ".join(x["text"] for x in current)))
    return cues


def caption_at(cues, t):
    return next((x[2] for x in cues if x[0] <= t <= x[1]), "")


def case_card(image, rank, channel, subscribers, example, views, estimate, note, t):
    c = Image.new("RGB", (W, CONTENT_H), (7, 10, 18))
    d = ImageDraw.Draw(c, "RGBA")
    d.rounded_rectangle((38, 28, 1242, 575), 28, fill=(15, 20, 33, 255), outline=(95, 116, 160, 180), width=2)
    im, pos = fit(image, (64, 110, 740, 520)); c.paste(im, pos)
    d.rounded_rectangle((760, 72, 1214, 530), 22, fill=(4, 7, 13, 235), outline=(79, 206, 255, 210), width=2)
    d.text((795, 101), f"CASE {rank}", font=font(20), fill=(78, 209, 255))
    d.text((795, 142), channel, font=font(34), fill="white")
    d.text((795, 205), f"구독자  {subscribers}", font=font(23), fill=(211, 219, 235))
    d.text((795, 248), f"대표 영상  {views}", font=font(23), fill=(211, 219, 235))
    d.text((795, 304), example, font=font(19), fill=(165, 178, 204))
    d.rounded_rectangle((790, 365, 1187, 431), 16, fill=(20, 49, 62, 255))
    d.text((988, 398), estimate, font=font(26), fill=(115, 235, 255), anchor="mm")
    d.text((795, 463), note, font=font(16), fill=(182, 188, 201))
    d.text((64, 62), "공개 AI 음악 플레이리스트 사례", font=font(26), fill=(242, 245, 251))
    return c


def mac_cafe(frames, t):
    c = Image.new("RGB", (W, CONTENT_H), (8, 12, 20)); d = ImageDraw.Draw(c, "RGBA")
    d.rounded_rectangle((70, 25, 1210, 585), 22, fill=(238, 239, 242), outline=(90, 97, 110), width=2)
    d.rounded_rectangle((70, 25, 1210, 77), 22, fill=(33, 36, 43))
    for x, color in [(101,(255,95,86)),(133,(255,189,46)),(165,(40,200,65))]: d.ellipse((x-8,43,x+8,59), fill=color)
    d.rounded_rectangle((300, 38, 985, 67), 13, fill=(53, 57, 66))
    d.text((642, 53), "cafe.naver.com/naverecho/865", font=font(15), fill=(229,232,237), anchor="mm")
    p = max(0, min(.999, (t-63.85)/10.0)); idx = min(2, int(p*3)); page=frames[idx]
    im, pos = fit(page, (86, 86, 1194, 565)); c.paste(im, pos)
    d.rounded_rectangle((90, 96, 455, 136), 18, fill=(4,8,14,225), outline=(75,210,255,220), width=2)
    d.text((272,116), "실제 카페 자료 안내 글", font=font(18), fill="white", anchor="mm")
    return c


def main(args):
    timing=json.loads(args.timings.read_text(encoding="utf-8")); duration=float(timing["audio_duration"]); cues=captions(timing["words"])
    cases={n:Image.open(args.cases/f"{n}.png").convert("RGB") for n in ["moonlight","hlkyw","aikmusic"]}
    cafes=[Image.open(args.cases/f"cafe-{i}.png").convert("RGB") for i in range(3)]
    cmd=[str(args.ffmpeg),"-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","-","-i",str(args.audio),"-map","0:v","-map","1:a","-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-shortest","-movflags","+faststart",str(args.output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    for fi in range(round(duration*FPS)):
        t=fi/FPS
        if t < 9.17:
            visual=Image.new("RGB",(W,CONTENT_H),(5,8,15)); d=ImageDraw.Draw(visual,"RGBA")
            d.text((W//2,205),"AI 음악 · AI 플리 자동화",font=font(48),fill="white",anchor="mm")
            d.text((W//2,280),"공개 채널 3곳으로 확인했습니다",font=font(34),fill=(86,218,255),anchor="mm")
            d.rounded_rectangle((360,350,920,418),20,fill=(17,48,62)); d.text((W//2,384),"조회수 · 음악 화면 · 수익 추정치",font=font(25),fill="white",anchor="mm")
        elif t < 24.25:
            visual=case_card(cases["moonlight"],1,"달빛라운지","약 6.2만","카페 음악 57집","19만 회","Nox 월 추정 약 20만 원","실제 정산액 아님 · Nox 제3자 추정",t)
        elif t < 36.72:
            visual=case_card(cases["hlkyw"],2,"Hlkyw Music","782명","AI 감성음악 플레이리스트","2.1만 회","공개 조회 성과","Nox 채널 금액 조회 불가",t)
        elif t < 48.51:
            visual=case_card(cases["aikmusic"],3,"AI K-뮤직","약 2.2천","AI 감성 음악 플레이","20만 회","공개 조회 성과","Nox 채널 금액 조회 불가",t)
        elif t < 63.85:
            visual=Image.new("RGB",(W,CONTENT_H),(5,8,15)); d=ImageDraw.Draw(visual,"RGBA")
            d.text((W//2,100),"같은 AI 음악이어도 결과는 달라집니다",font=font(38),fill="white",anchor="mm")
            items=["주제와 장르","썸네일·제목","시청 지속 시간","저작권·수익화 심사"]
            for i,item in enumerate(items):
                x=170+(i%2)*500;y=190+(i//2)*150
                d.rounded_rectangle((x,y,x+440,y+105),22,fill=(14,29,45),outline=(57,198,244),width=2)
                d.text((x+220,y+52),item,font=font(27),fill=(230,239,247),anchor="mm")
        elif t < 74.0:
            visual=mac_cafe(cafes,t)
        else:
            visual=Image.new("RGB",(W,CONTENT_H),(5,8,15)); d=ImageDraw.Draw(visual,"RGBA")
            d.text((W//2,170),"수익 보장이 아니라",font=font(38),fill=(188,198,214),anchor="mm")
            d.text((W//2,245),"반복 제작을 줄이고",font=font(48),fill="white",anchor="mm")
            d.text((W//2,315),"반응을 빠르게 검증하는 시스템",font=font(42),fill=(83,221,255),anchor="mm")
            d.text((W//2,430),"AI 음악 + 플레이리스트 자동화",font=font(30),fill=(220,227,240),anchor="mm")
        canvas=Image.new("RGB",(W,H),(3,5,10));canvas.paste(visual,(0,0)); d=ImageDraw.Draw(canvas,"RGBA")
        d.rectangle((0,CONTENT_H,W,H),fill=(3,5,10,250)); d.line((0,CONTENT_H,W,CONTENT_H),fill=(52,60,78),width=1)
        cap=caption_at(cues,t)
        if cap:
            d.text((W//2+2,667+2),cap,font=font(28),fill=(0,0,0,220),anchor="mm")
            d.text((W//2,667),cap,font=font(28),fill=(248,248,245),anchor="mm")
        proc.stdin.write(canvas.tobytes())
    proc.stdin.close()
    if proc.wait(): raise SystemExit("ffmpeg failed")


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--cases",type=Path,required=True);p.add_argument("--audio",type=Path,required=True);p.add_argument("--timings",type=Path,required=True);p.add_argument("--output",type=Path,required=True);p.add_argument("--ffmpeg",type=Path,required=True);main(p.parse_args())
