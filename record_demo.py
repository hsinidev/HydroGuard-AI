"""
HydroGuard AI — Automated Playwright Demo Recorder with Synchronized AI Voiceover
Module: record_demo.py
Description: Synthesizes edge-tts narration, records 1080p browser walkthrough, and merges with FFmpeg.
"""

import os
import sys
import time
import asyncio
import subprocess
import edge_tts
from playwright.async_api import async_playwright

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "demo_video_output"))
TEMP_DIR = os.path.join(OUTPUT_DIR, "temp")
FINAL_MP4 = os.path.join(OUTPUT_DIR, "demo.mp4")

VOICE = "en-US-ChristopherNeural"

NARRATION_SCRIPTS = [
    (
        "clip1.mp3",
        "Welcome to HydroGuard AI, an industrial predictive maintenance, diagnostic, and safety orchestration platform for multistage centrifugal pumps, architected by Mohamed Hsini."
    ),
    (
        "clip2.mp3",
        "Opening Engine Settings. Here, reliability engineers manage Google Gemini models and inspect the lead architect credentials and safety boundaries."
    ),
    (
        "clip3.mp3",
        "Now observing Pump P-204 under suction starvation. Deterministic hydraulic calculations identify a critical NPSH margin deficit of zero point one meters. Simultaneously, frequency-domain FFT analysis detects elevated broadband energy in the 1 to 5 kilohertz cavitation zone."
    ),
    (
        "clip4.mp3",
        "The dynamic Bayesian engine ranks Cavitation as the top hypothesis. The operator executes the Next-Best-Verification step, inputting strainer differential pressure, and generates an exportable ISO 55000 work order complete with bill of materials and OSHA Lockout Tagout procedures."
    )
]

async def generate_narration_audio():
    os.makedirs(TEMP_DIR, exist_ok=True)
    audio_files = []
    print("Generating narration audio clips...")
    for idx, (filename, text) in enumerate(NARRATION_SCRIPTS):
        filepath = os.path.join(TEMP_DIR, filename)
        wav_path = os.path.join(TEMP_DIR, f"clip{idx+1}.wav")
        try:
            communicate = edge_tts.Communicate(text, VOICE)
            await communicate.save(filepath)
            audio_files.append(filepath)
            print(f"  Generated {filename} (edge-tts)")
        except Exception as e:
            # Robust Windows Native SAPI Speech Synthesizer fallback
            print(f"  edge-tts offline, using Windows SAPI TTS for {filename}...")
            norm_wav = wav_path.replace("\\", "/")
            clean_text = text.replace("'", "")
            ps_script = f'''
            Add-Type -AssemblyName System.Speech
            $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $synth.SelectVoiceByHints([System.Speech.Synthesis.VoiceGender]::Male)
            $synth.SetOutputToWaveFile('{norm_wav}')
            $synth.Speak('{clean_text}')
            $synth.Dispose()
            '''
            subprocess.run(["powershell", "-Command", ps_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Convert WAV to MP3 with FFmpeg
            subprocess.run(["ffmpeg", "-y", "-i", wav_path, "-c:a", "libmp3lame", "-b:a", "192k", filepath], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            audio_files.append(filepath)
            print(f"  Generated {filename} (Windows SAPI)")
    
    # Merge audio clips with silence gaps using FFmpeg
    concat_list_file = os.path.join(TEMP_DIR, "audio_concat.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for af in audio_files:
            clean_af = af.replace("\\", "/")
            f.write(f"file '{clean_af}'\n")

    merged_audio = os.path.join(TEMP_DIR, "full_narration.mp3")
    cmd = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_list_file,
        "-c", "copy", merged_audio
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("Merged narration audio created:", merged_audio)
    return merged_audio

async def record_playwright_browser():
    os.makedirs(TEMP_DIR, exist_ok=True)
    print("Starting Playwright Chromium recording at 1920x1080...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--start-maximized", "--no-sandbox"]
        )
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=TEMP_DIR,
            record_video_size={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        # Navigate to local SCADA workstation
        print("Navigating to http://127.0.0.1:8000...")
        await page.goto("http://127.0.0.1:8000", wait_until="domcontentloaded", timeout=15000)
        await page.wait_for_timeout(3000)

        # 1. Open Engine Settings & Dev Info Modal
        print("Interacting with Engine Settings & Developer Info Modal...")
        settings_btn = page.locator("button:has-text('Engine Settings')")
        if await settings_btn.count() > 0:
            await settings_btn.click()
            await page.wait_for_timeout(4000)
            
            # Close Modal
            close_btn = page.locator("button:has-text('Close')")
            if await close_btn.count() > 0:
                await close_btn.click()
            await page.wait_for_timeout(1500)

        # 2. Inspect Vector Gauges & Spectrum
        print("Inspecting live vector gauges and FFT vibration spectrum...")
        await page.mouse.move(300, 200)
        await page.wait_for_timeout(1000)
        await page.mouse.move(600, 200)
        await page.wait_for_timeout(1000)
        await page.mouse.move(500, 450)
        await page.wait_for_timeout(3000)

        # 3. Expand Top Hypothesis Card
        print("Expanding top Cavitation hypothesis evidence trail...")
        hypo_card = page.locator("div:has-text('Cavitation / Vapor Bubble')").first
        if await hypo_card.count() > 0:
            await hypo_card.click()
            await page.wait_for_timeout(3500)

        # 4. Fill in Next-Best-Verification Reading
        print("Submitting technician field verification reading...")
        input_field = page.locator("input[placeholder*='measurement']")
        if await input_field.count() > 0:
            await input_field.fill("0.42")
            await page.wait_for_timeout(1000)
            submit_btn = page.locator("button:has-text('Submit')")
            if await submit_btn.count() > 0:
                await submit_btn.click()
                await page.wait_for_timeout(3000)

        # 5. Open ISO 55000 Work Order Modal
        print("Opening ISO 55000 Maintenance Work Order modal...")
        wo_btn = page.locator("button:has-text('ISO 55000 Work Order')").first
        if await wo_btn.count() > 0:
            await wo_btn.click()
            await page.wait_for_timeout(4500)
            
            # Close WO Modal
            wo_close = page.locator("button svg.lucide-x").first
            if await wo_close.count() > 0:
                await wo_close.click()
            await page.wait_for_timeout(1500)

        # 6. Switch to another scenario (Shaft Misalignment)
        print("Switching scenario to Shaft Misalignment...")
        misalign_btn = page.locator("button:has-text('Case 17')")
        if await misalign_btn.count() > 0:
            await misalign_btn.click()
            await page.wait_for_timeout(3500)

        # 7. Switch to Healthy Baseline
        print("Switching scenario to Healthy Baseline...")
        healthy_btn = page.locator("button:has-text('Case 29')")
        if await healthy_btn.count() > 0:
            await healthy_btn.click()
            await page.wait_for_timeout(3000)

        # Close page and context to flush video file
        video_path = await page.video.path()
        await page.close()
        await context.close()
        await browser.close()
        print("Playwright video captured at:", video_path)
        return video_path

def post_process_video(video_path: str, audio_path: str):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Post-processing video and audio into {FINAL_MP4} via FFmpeg...")
    
    # Merge video and audio with 1080p standard H.264 / AAC
    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        FINAL_MP4
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0:
        print(f"SUCCESS: Final 1080p demonstration video created at:\n  {FINAL_MP4}")
    else:
        print("FFmpeg warning, attempting fallback muxing...")
        cmd_fallback = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            FINAL_MP4
        ]
        subprocess.run(cmd_fallback)
        print(f"Fallback video created at {FINAL_MP4}")

async def main():
    # 1. Generate Voiceover Audio
    audio_path = await generate_narration_audio()
    
    # 2. Record Browser Walkthrough
    video_path = await record_playwright_browser()
    
    # 3. Post-process into 1080p MP4
    post_process_video(video_path, audio_path)

if __name__ == "__main__":
    asyncio.run(main())
