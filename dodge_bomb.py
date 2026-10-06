import os
import random
import sys
import pygame as pg
import time


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー時に画面をブラックアウトし、
    「Game Over」の文字と泣いているこうかとんを表示する関数
    引数 screen: 画面Surface
    戻り値: なし
    """
    # 1 & 2. 半透明の黒い画面（Surface）を作成
    black_out = pg.Surface((WIDTH, HEIGHT))
    black_out.fill((0, 0, 0))
    black_out.set_alpha(200)  # 透明度の設定（0〜255）

    # 3. 白文字で「Game Over」のフォントSurfaceを作成
    font = pg.font.Font(None, 80)
    txt_img = font.render("Game Over", True, (255, 255, 255))
    txt_rct = txt_img.get_rect()
    txt_rct.center = WIDTH // 2, HEIGHT // 2

    # 4. 泣いているこうかとん（8.png）のSurfaceを作成
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    cry_rct1 = cry_img.get_rect()
    cry_rct1.center = WIDTH // 2 - 200, HEIGHT // 2
    cry_rct2 = cry_img.get_rect()
    cry_rct2.center = WIDTH // 2 + 200, HEIGHT // 2

    # テキストとこうかとんを黒いSurfaceに貼り付ける
    black_out.blit(txt_img, txt_rct)
    black_out.blit(cry_img, cry_rct1)
    black_out.blit(cry_img, cry_rct2)

    # 5. 画面に表示して更新
    screen.blit(black_out, [0, 0])
    pg.display.update()

    # 6. 5秒間停止
    time.sleep(5)

def check_bound(rect: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんまたは爆弾のRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue／画面外ならFalse
    """
    yoko, tate = True, True
    if rect.left < 0 or WIDTH < rect.right:  # 横方向判定
        yoko = False
    if rect.top < 0 or HEIGHT < rect.bottom:  # 縦方向判定
        tate = False
    return yoko, tate
    

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 練習2：空のSurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 練習2：赤い爆弾
    bb_img.set_colorkey((0, 0, 0))  # 練習2：四隅の黒い部分を透過する
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)  # 横座標用の乱数
    bb_rct.centery = random.randint(0, HEIGHT)  # 縦座標用の乱数
    vx, vy = +5, +5  # 練習2：爆弾の初期速度
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(bb_rct):  # 練習4：kkとbbのrectが重なっていたら
            gameover(screen)  # ゲームオーバー画面を表示
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, tpl in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += tpl[0]  # 横方向移動量
                sum_mv[1] += tpl[1]  # 縦方向移動量
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # どこからしらはみ出てる
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])  # 先程の動きをキャンセルする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)  # 練習2：爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # yoko == False
            vx *= -1
        if not tate:  # tate == False
            vy *= -1
        screen.blit(bb_img, bb_rct)  # 練習2：爆弾表示
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()