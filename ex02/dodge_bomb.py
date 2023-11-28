import sys
import pygame as pg
import random
WIDTH, HEIGHT = 1600, 900

delta = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:

    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02-20231128/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02-20231128/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5
    delta1 = {
        (0, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 90, 1),
        (0, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -90, 1),
        (+5, 0): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 0, 1),
        (-5, 0): pg.transform.rotozoom(kk_img, 0, 1),
        (-5, -5): pg.transform.rotozoom(kk_img, -45, 1),
        (-5, +5): pg.transform.rotozoom(kk_img, 45, 1),
        (+5, -5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), 45, 1),
        (+5, +5): pg.transform.rotozoom(pg.transform.flip(kk_img, True, False), -45, 1)
    }

    clock = pg.time.Clock()
    tmr = 0
    count = 1000000
    accs = [a for a in range(1, 11)]
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bb_imgs.append(bb_img)
    bb_img = bb_imgs[min(tmr//500, 9)]
    bb_img.set_colorkey((0, 0, 0))
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        if tuple(sum_mv) in delta1.keys():
            kk_img = delta1[tuple(sum_mv)]

        screen.blit(bg_img, [0, 0])
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        if kk_rct.colliderect(bb_rct):
            kk_img = pg.image.load("ex02-20231128/fig/8.png")
            kk_img = pg.transform.rotozoom(kk_img, 0, 2)

            count = tmr
        avx, avy = vx*accs[min(tmr//500, 9)], vy*accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_img.set_colorkey((0, 0, 0))
        bb_rct.move_ip(avx, avy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        if tmr == count + 2:
            return


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
