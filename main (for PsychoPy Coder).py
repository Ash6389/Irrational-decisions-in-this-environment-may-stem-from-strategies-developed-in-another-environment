"""
World-switch evidence-sampling task (PsychoPy).

Run from this folder:
    python main.py                      # dialog asks for participant ID, session, condition
    python main.py --participant 7      # skip the dialog
    python main.py --windowed           # 1280 x 720 window instead of full screen

Press Esc at any time to stop; everything collected so far is already saved.
"""

import argparse

from psychopy import core, logging, visual

import config as cfg
from data_io import DataLog
from display import QuitSession
from procedure import Session
from task_logic import build_schedule, condition_from, make_rng


def parse_args():
    p = argparse.ArgumentParser(description='World-switch evidence-sampling task')
    p.add_argument('--participant', help='participant ID (skips the dialog)')
    p.add_argument('--session', default='1', help='session label (default 1)')
    p.add_argument('--condition', type=int, choices=[1, 2, 3, 4],
                   help='counterbalancing condition 1-4 (default: taken from the participant ID)')
    p.add_argument('--windowed', action='store_true', help='run in a window instead of full screen')
    return p.parse_args()


def ask_session_info():
    """PsychoPy dialog; falls back to the console if no GUI toolkit is available."""
    fields = {'Participant ID': '', 'Session': '1', 'Condition (1-4, blank = from ID)': ''}
    try:
        from psychopy import gui
        dlg = gui.DlgFromDict(fields, title='World-switch task', order=list(fields))
        if not dlg.OK:
            core.quit()
    except ImportError:
        fields['Participant ID'] = input('Participant ID: ')
        fields['Session'] = input('Session [1]: ') or '1'
        fields['Condition (1-4, blank = from ID)'] = input('Condition 1-4 [from ID]: ')
    raw_condition = str(fields['Condition (1-4, blank = from ID)']).strip()
    return (str(fields['Participant ID']).strip() or 'test', str(fields['Session']).strip() or '1',
            int(raw_condition) if raw_condition in ('1', '2', '3', '4') else None)


def main():
    args = parse_args()
    if args.participant:
        participant, session, condition = args.participant, args.session, args.condition
    else:
        participant, session, condition = ask_session_info()
    condition = condition or condition_from(participant)

    rng = make_rng(participant, session)
    schedule = build_schedule(condition, rng)
    info = {'participant': participant, 'session': session}
    log = DataLog(info, schedule['_meta'])

    logging.console.setLevel(logging.WARNING)
    fullscreen = cfg.FULLSCREEN and not args.windowed
    win = visual.Window(size=cfg.WINDOW_SIZE, fullscr=fullscreen, screen=cfg.SCREEN_INDEX,
                        units='height', color=cfg.COL['bg'], allowGUI=not fullscreen)

    task, status = None, 'not started'
    try:
        task = Session(win, schedule, log, rng)
        status = task.run()
    except QuitSession:
        status = 'aborted (quit key)'
    finally:
        log.close(status=status,
                  main_points=round(task.points, 2) if task else None,
                  baseline_points=task.baseline_points if task else None,
                  probes_answered=task.probe_count if task else None)
        win.close()
        core.quit()


if __name__ == '__main__':
    main()
