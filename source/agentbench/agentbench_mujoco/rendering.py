"""Optional headless rendering and run recording."""
import os
import sys
from pathlib import Path


def configure_headless():
    # Respect an explicit renderer choice, including GPU EGL or OSMesa.
    mesa=Path('/usr/share/glvnd/egl_vendor.d/50_mesa.json')
    if sys.platform.startswith('linux') and 'MUJOCO_GL' not in os.environ and mesa.exists():
        os.environ['MUJOCO_GL']='egl'
        os.environ.setdefault('PYOPENGL_PLATFORM','egl')
        os.environ.setdefault('EGL_PLATFORM','surfaceless')
        os.environ.setdefault('__EGL_VENDOR_LIBRARY_FILENAMES',str(mesa))


class Recorder:
    def __init__(self,path,fps=25,playback_speed=1.):
        import imageio.v2 as imageio
        if not 1<=fps<=60 or not .25<=playback_speed<=8:
            raise ValueError('Capture fps must be 1–60 and playback speed 0.25–8')
        self.output_fps=fps*playback_speed
        self.writer=imageio.get_writer(path,fps=self.output_fps,codec='libx264',quality=8,macro_block_size=1)
        self.next_time=0.;self.period=1/fps;self.frames=0

    def __call__(self,env,label=''):
        if env.data.time+1e-8<self.next_time:return
        self.writer.append_data(annotated_frame(env,label))
        self.frames+=1
        self.next_time+=self.period

    def close(self):
        self.writer.close()

    def finish(self,env,label):
        # Always show the actual terminal state, even between capture ticks.
        # One second of held display time does not advance the simulator.
        frame=annotated_frame(env,label)
        for _ in range(max(1,round(self.output_fps))):
            self.writer.append_data(frame)
            self.frames+=1


def annotated_frame(env,label=''):
    """Presentation HUD for developer recordings; not used by Vision observations."""
    import numpy as np
    from PIL import Image,ImageDraw,ImageFont,ImageColor
    from .campaign_scene import SCENARIOS,TIERS
    img=Image.fromarray(env.render())
    d=ImageDraw.Draw(img,'RGBA');w,h=img.size
    path=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    bold=path.with_name('DejaVuSans-Bold.ttf')
    def font(size,strong=False):
        p=bold if strong else path
        return ImageFont.truetype(str(p),size) if p.exists() else ImageFont.load_default()
    scale=w/960
    title_font=font(round(25*scale),True);small=font(round(13*scale))
    tiny=font(round(11*scale));stat=font(round(18*scale),True)
    margin=round(24*scale);top=round(86*scale);bottom=round(74*scale)
    ink=(31,48,53);muted=(94,113,118)
    cfg=SCENARIOS.get(getattr(env,'scenario',''))
    accent=ImageColor.getrgb(TIERS[cfg['tier']]['color']) if cfg else (63,128,145)
    d.rectangle((0,0,w,top),fill=(245,247,241,248))
    d.rectangle((0,0,round(6*scale),top),fill=accent)
    d.text((margin,round(12*scale)),'MARBLE LAB  /  DUAL FRANKA' if env.dual_arm else 'MARBLE LAB  /  FRANKA',font=small,fill=muted)
    title=cfg['title'] if cfg else env.level.replace('_',' ').title()
    d.text((margin,round(33*scale)),title,font=title_font,fill=ink)
    badge=f"{cfg['stage']}  /  {TIERS[cfg['tier']]['title'].upper()}" if cfg else 'CONTACT PHYSICS'
    bw=d.textbbox((0,0),badge,font=small)[2]+round(30*scale)
    d.rounded_rectangle((w-margin-bw,round(16*scale),w-margin,round(46*scale)),radius=round(8*scale),fill=accent)
    d.text((w-margin-bw+round(15*scale),round(23*scale)),badge,font=small,fill='white')
    mode='PRELOADED' if env.initial_mode=='loaded' else 'PICK UP FROM FLOOR'
    if cfg and getattr(env,'target_profile','authored')!='authored':
        mode=getattr(env,'target_profile','').upper()+' PIGS  /  '+mode
    mw=d.textbbox((0,0),mode,font=tiny)[2]
    d.text((w-margin-mw,round(56*scale)),mode,font=tiny,fill=muted)
    if cfg and (getattr(env,'variation','nominal')!='nominal' or getattr(env,'background','park')!='park'):
        setting=f"{env.background.upper()}  /  {env.variation.upper()}"
        d.text((margin,round(66*scale)),setting,font=tiny,fill=muted)
    d.rectangle((0,h-bottom,w,h),fill=(245,247,241,248))
    y=h-bottom+round(12*scale)
    if hasattr(env,'target_alive'):
        required=getattr(env,'required_indices',list(range(len(env.target_alive))))
        stats=[(f'{sum(~env.target_alive[required])} / {len(required)}','TARGETS CLEARED'),
               (f'{len(env.shots)} / {len(env.ammo_ids)}','SHOTS USED')]
    else:stats=[('CLEARED' if env.success else env.phase.upper(),'STATUS')]
    for i,(value,caption) in enumerate(stats):
        x=margin+i*round(165*scale)
        d.text((x,y),value,font=stat,fill=ink)
        d.text((x,y+round(26*scale)),caption,font=tiny,fill=muted)
    x=round(370*scale)
    d.text((x,y),label or env.phase.title(),font=small,fill=ink)
    angle=f'  /  {30+np.rad2deg(env.data.qpos[env.elevation_q]):.1f} deg' if env.dual_arm else ''
    d.text((x,y+round(23*scale)),f'{env.data.time:.2f} s{angle}  /  draw {env.data.qpos[env.draw_q]*100:.1f} cm',font=tiny,fill=muted)
    note='MuJoCo | developer baseline'
    nw=d.textbbox((0,0),note,font=tiny)[2]
    d.text((w-margin-nw,h-round(20*scale)),note,font=tiny,fill=muted)
    return np.asarray(img)
