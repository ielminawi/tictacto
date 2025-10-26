from openai import OpenAI
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
import json, os, time
import webbrowser
from pathlib import Path
import numpy as np
import requests
from io import BytesIO

# Try to import optional dependencies
try:
    from moviepy.editor import *
    from PIL import Image, ImageDraw, ImageFont
    import textwrap
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

# Reel generation models
class ReelScript(BaseModel):
    title: str
    hook: str  # Opening line to grab attention
    main_content: List[str]  # Key points to cover
    call_to_action: str
    hashtags: List[str]
    duration_seconds: int = 30
    visual_descriptions: List[str]  # What should be shown on screen
    music_style: str = "upbeat, modern"
    target_audience: str = "general"

class ReelVideo(BaseModel):
    script: ReelScript
    video_prompts: List[str]  # Prompts for Sora2 video generation
    thumbnail_prompt: str
    captions: List[str]  # Text overlays for each scene

class ReelGenerator:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.current_script = None
        
    def extract_pdf_content(self, pdf_path: str) -> str:
        """Extract text content from PDF"""
        try:
            # Upload PDF to OpenAI
            pdf_file = self.client.files.create(file=open(pdf_path, "rb"), purpose="assistants")
            
            prompt = ("Extract all the most important information from this PDF."
                      "Focus on persons, companies and their relations.")
            
            # Use the same API format as kg4.py
            response = self.client.responses.parse(
                model="gpt-5",
                input=[{
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {"type": "input_file", "file_id": pdf_file.id}
                    ]
                }],
                max_output_tokens=10000
            )
            
            return response.output_text
            
        except Exception as e:
            print(f"Error extracting PDF content: {e}")
            return ""
    
    def generate_direct_video_prompt(self, content: str) -> str:
        """Generate a direct Sora video prompt from PDF content"""
        
        prompt = f"""
        Create a compelling 15-second Instagram Reel video prompt from this content:
        
        CONTENT:
        {content}
        
        Create a single, engaging video prompt that:
        1. Starts with an attention-grabbing hook (first 3 seconds)
        2. Shows the most important information clearly
        3. Ends with a call-to-action
        4. Is optimized for Instagram Reels (vertical format)
        5. Uses modern, trending visual style
        6. Includes animated text overlays
        7. Has dynamic camera movement
        8. Uses bright, vibrant lighting
        
        Format the response as a single video prompt for Sora that can be used directly.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating video prompt: {e}")
            # Return default prompt if generation fails
            return f"""
            A dynamic 15-second Instagram Reel video showing key insights from: {content[:200]}...
            Style: Modern, engaging, high energy
            Format: Vertical (9:16 aspect ratio)
            Camera: Dynamic movement, close-up to medium shots
            Lighting: Bright, vibrant, social media optimized
            Text: Animated overlays with key information
            Mood: Exciting, informative, shareable
            """
    
    def generate_video_prompts(self, script: ReelScript) -> List[str]:
        """Generate Sora video generation prompts from script"""
        
        video_prompts = []
        
        # Hook scene - dynamic and engaging
        hook_prompt = f"""
        A dynamic, fast-paced 8-second video for Instagram Reel. 
        {script.visual_descriptions[0] if script.visual_descriptions else "Modern, vibrant visual with animated text overlay"}
        Style: High energy, trending, social media optimized
        Camera: Dynamic movement, close-up to medium shot
        Lighting: Bright, colorful, modern
        Text: "{script.hook}" appears with animation
        Mood: Exciting, attention-grabbing
        """
        video_prompts.append(hook_prompt.strip())
        
        # Main content scenes
        for i, content in enumerate(script.main_content[:3]):  # Limit to 3 main points
            visual_desc = script.visual_descriptions[i+1] if i+1 < len(script.visual_descriptions) else "Professional, educational presentation"
            content_prompt = f"""
            An engaging 8-second educational video for Instagram Reel.
            {visual_desc}
            Style: Clean, professional, informative
            Camera: Smooth transitions, medium shot
            Lighting: Well-lit, professional
            Text: "{content}" appears clearly on screen
            Mood: Educational, trustworthy
            """
            video_prompts.append(content_prompt.strip())
        
        # Call-to-action scene
        cta_prompt = f"""
        A motivational 8-second call-to-action video for Instagram Reel.
        {script.visual_descriptions[-1] if script.visual_descriptions else "Inspiring, action-oriented visual"}
        Style: Motivational, clear, engaging
        Camera: Medium to wide shot, confident framing
        Lighting: Bright, inspiring
        Text: "{script.call_to_action}" with emphasis
        Mood: Motivational, encouraging action
        """
        video_prompts.append(cta_prompt.strip())
        
        return video_prompts
    
    def generate_direct_sora_video(self, video_prompt: str, client: OpenAI) -> str:
        """Generate a 12-second video with Sora and save locally"""
        print("🎬 Generating 12-second video with Sora...")
        print(f"Prompt: {video_prompt}...")

        video = client.videos.create(
            model="sora-2-pro",
            prompt=video_prompt,
            seconds="12",
            size="720x1280",
            # quality="hd",  # enable if your org supports it
        )
        print("Created video job:", video.id, "→ status:", video.status)
        print(video)
        # Wait until Sora finishes rendering
        terminal = {"succeeded", "completed", "failed", "error", "canceled"}
        start = time.time()
        while video.status not in terminal:
            print(f"status={video.status}, progress={getattr(video, 'progress', 0)}, object={video.object}")
            time.sleep(10)
            video = client.videos.retrieve(video.id)   # refresh object
            if time.time() - start > 900:
                raise TimeoutError("⏰ Video job stuck >15 minutes.")


        # Re-fetch to make sure the job is marked completed
        video = client.videos.retrieve(video.id)
        print("Job completed. Fetching associated files...")

        # 4️⃣ Download it directly from the Files endpoi
        content = client.videos.download_content(video.id, variant="video")
        content.write_to_file("video.mp4")


        print(f"✅ Video downloaded and saved as video.mp4")


        # print(f"📦 Downloading from: {video_url}")

        # # Download and save video locally
        # video_response = requests.get(video_url)
        # video_filename = "direct_sora_reel.mp4"
        # with open(video_filename, "wb") as f:
        #     f.write(video_response.content)

        # print(f"✅ Video saved as {video_filename}")
        # return video_filename
    
    def combine_sora_videos(self, video_urls: List[str], script: ReelScript) -> str:
        """Combine individual Sora videos into a final reel"""
        print("🎬 Combining Sora videos into final reel...")
        
        if not MOVIEPY_AVAILABLE:
            print("❌ MoviePy not installed. Install with: pip install moviepy")
            return "moviepy_not_available.mp4"
        
        
            
        clips = []
        for i, video_url in enumerate(video_urls):
            if video_url.startswith("http"):
                # Download video if it's a URL
                video_response = requests.get(video_url)
                temp_filename = f"temp_sora_{i}.mp4"
                with open(temp_filename, "wb") as f:
                    f.write(video_response.content)
                clip = VideoFileClip(temp_filename)
            else:
                # Local file
                clip = VideoFileClip(video_url)
                
            clips.append(clip)
            
        # Combine all clips
        final_video = concatenate_videoclips(clips)
            
        # Add fade transitions between clips
        final_video = final_video.fadein(0.5).fadeout(0.5)
            
        # Export final reel
        output_path = "final_sora_reel.mp4"
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
            
        print(f"✅ Final reel created: {output_path}")
        return output_path
            
        
    def create_reel_html(self, reel_video: ReelVideo, video_urls: List[str]) -> str:
        """Create an HTML preview of the reel"""
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Generated Reel: {reel_video.script.title}</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
            <style>
                body {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    min-height: 100vh;
                }}
                
                .reel-container {{
                    background: white;
                    border-radius: 20px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                    overflow: hidden;
                    margin: 20px auto;
                    max-width: 400px;
                }}
                
                .reel-header {{
                    background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                }}
                
                .reel-title {{
                    font-size: 1.5rem;
                    font-weight: bold;
                    margin-bottom: 10px;
                }}
                
                .reel-hook {{
                    font-size: 1.1rem;
                    opacity: 0.9;
                }}
                
                .script-content {{
                    padding: 20px;
                }}
                
                .content-point {{
                    background: #f8f9fa;
                    border-left: 4px solid #ff6b6b;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 0 10px 10px 0;
                }}
                
                .cta-section {{
                    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
                    color: white;
                    padding: 20px;
                    text-align: center;
                    margin: 20px 0;
                    border-radius: 10px;
                }}
                
                .hashtags {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 5px;
                    margin-top: 15px;
                }}
                
                .hashtag {{
                    background: #e9ecef;
                    color: #495057;
                    padding: 5px 10px;
                    border-radius: 15px;
                    font-size: 0.9rem;
                }}
                
                .video-preview {{
                    background: #000;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    margin: 10px 0;
                    border-radius: 10px;
                }}
                
                .stats {{
                    display: flex;
                    justify-content: space-around;
                    padding: 15px;
                    background: #f8f9fa;
                }}
                
                .stat-item {{
                    text-align: center;
                }}
                
                .stat-number {{
                    font-size: 1.5rem;
                    font-weight: bold;
                    color: #ff6b6b;
                }}
                
                .stat-label {{
                    font-size: 0.9rem;
                    color: #6c757d;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="reel-container">
                    <div class="reel-header">
                        <div class="reel-title">{reel_video.script.title}</div>
                        <div class="reel-hook">{reel_video.script.hook}</div>
                    </div>
                    
                    <div class="script-content">
                        <h5><i class="fas fa-list"></i> Main Content</h5>
                        {''.join([f'<div class="content-point"><strong>Point {i+1}:</strong> {point}</div>' for i, point in enumerate(reel_video.script.main_content)])}
                        
                        <div class="cta-section">
                            <h5><i class="fas fa-bullhorn"></i> Call to Action</h5>
                            <p>{reel_video.script.call_to_action}</p>
                        </div>
                        
                        <h5><i class="fas fa-video"></i> Video Scenes</h5>
                        {''.join([f'<div class="video-preview"><strong>Scene {i+1}:</strong> {prompt[:100]}...</div>' for i, prompt in enumerate(reel_video.video_prompts)])}
                        
                        <div class="hashtags">
                            {''.join([f'<span class="hashtag">{tag}</span>' for tag in reel_video.script.hashtags])}
                        </div>
                    </div>
                    
                    <div class="stats">
                        <div class="stat-item">
                            <div class="stat-number">{reel_video.script.duration_seconds}s</div>
                            <div class="stat-label">Duration</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{len(reel_video.script.main_content)}</div>
                            <div class="stat-label">Key Points</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-number">{len(video_urls)}</div>
                            <div class="stat-label">Scenes</div>
                        </div>
                    </div>
                </div>
                
                <div class="text-center mt-4">
                    <button class="btn btn-primary btn-lg" onclick="generateReel()">
                        <i class="fas fa-magic"></i> Generate Full Reel
                    </button>
                </div>
            </div>
            
            <script>
                function generateReel() {{
                    alert('Reel generation complete! Check the generated files.');
                }}
            </script>
        </body>
        </html>
        """
        
        return html_content

def main():
    # Initialize with the same API key as kg4.py
    API_KEY = "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"
    
    generator = ReelGenerator(API_KEY)
    
    print("🎬 Instagram Reel Generator")
    print("=" * 50)
            # 1️⃣ Get all files in your account (limit=5 for convenience)
    # files = generator.client.files.list(limit=5)
    # print(files, " \n")


    # video = generator.client.videos.retrieve("video_68fd4886266881909a9c635bb549b9fd07651b279bfd4e84")
    # content = generator.client.videos.download_content("video_68fd4886266881909a9c635bb549b9fd07651b279bfd4e84", variant="video")
    # content.write_to_file("video.mp4")
    # raw = video

    # print(raw)
    # file_id = video.model_dump().get("result", {}).get("id")
    #     if file_id:
    #         content = client.videos.content(file_id)
    #         with open("direct_sora_reel.mp4", "wb") as f:
    #             f.write(content)

    # 2️⃣ Print them to see which belongs to this video
    # for f in files.data:
    #     print(f.id, f.created_at, "\n")
    
    # # Extract content from PDF
    # print("📄 Extracting content from PDF...")
    # pdf_path = "pdf_test2.pdf"
    # content = generator.extract_pdf_content(pdf_path)
    
    # if not content:
    #     print("❌ Failed to extract content from PDF")
    #     return
    
    # print(f"✅ Extracted {len(content)} characters from PDF")
    
    # # Generate direct video prompt from content
    # print("✍️ Creating direct video prompt...")
    # video_prompt = generator.generate_direct_video_prompt(content)
    
    # print(f"✅ Generated video prompt:")
    # print(f"   {video_prompt[:200]}...")

    video_prompt = """
    Create a short, funny 15-second video that summarizes this account report for TechParts GmbH as if it were a comedy sketch.
    Show a stressed-out account manager trying to keep Martin Vogel, the picky purchasing lead, happy.
    Mention that Martin wants Net 30 days payment, we insist on Net 45, and that he nearly moved half his business to Altus Components because of late shipments.
    Include the €7.2 K credit note, the fragile ‘yellow’ relationship health, and Martin’s hatred for long apology emails.
    Make it playful - like a dramatic corporate soap-opera trailer called ‘Days of Our POs’ - ending with the line:
    ‘Dispatch Thursdays decide our fate!’
    """

    video_prompt2 = """Create a concise, 12-second video introducing Martin Vogel, the purchasing lead managing the TechParts account.
    Show him as a sharp but frustrated buyer dealing with delayed deliveries and payment disputes — he wants Net 30, TechParts insists on Net 45.
    Add a quick, dramatic moment where he threatens to move half the business to rival Altus Components, followed by TechParts issuing a €7.2 K credit note to keep him happy.
    End with the tagline on screen:
    ‘Martin Vogel — the buyer who keeps TechParts on their toes."""

    video_prompt3 = """Create a 12-second informative video introducing Martin Vogel, the purchasing lead responsible for the TechParts GmbH account.
    Explain that he oversees supply performance, payment terms, and relationship health between TechParts and his company.
    Mention that recent delivery delays and differing payment expectations (Net 30 vs. Net 45 days) caused tension, leading Martin to consider shifting part of the business to Altus Components."""

    
    # video_prompt = """
    # Create a video with a tiger for children
    # """

    # Generate single 15-second video directly with Sora
    print("🎬 Generating direct video with Sora...")
    video_filename = generator.generate_direct_sora_video(video_prompt3, generator.client)
    
    # Create simple HTML preview
    print("🌐 Creating HTML preview...")
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generated Reel</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            video {{ width: 100%; max-width: 400px; border-radius: 10px; }}
            .info {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 Generated Instagram Reel</h1>
            <video controls>
                <source src="video.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="info">
                <h3>Video Details:</h3>
                <p><strong>Duration:</strong> 15 seconds</p>
                <p><strong>Format:</strong> Vertical (9:16) - Instagram Reels optimized</p>
                <p><strong>Generated from:</strong> PDF content</p>
                <p><strong>AI Model:</strong> Sora</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Save HTML file
    with open("reel_preview.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Save video prompt as text
    with open("video_prompt.txt", "w", encoding="utf-8") as f:
        f.write(video_prompt3)
    
    print("\n🎉 Direct Video Generation Complete!")
    print("=" * 50)
    print(f"🎥 Video file: {video_filename}")
    print(f"📝 Video prompt saved to: video_prompt.txt")
    print(f"🌐 Preview saved to: reel_preview.html")
    print(f"⏱️ Duration: 15 seconds")
    print(f"📱 Format: Vertical (Instagram Reels optimized)")
    
    if video_filename and not video_filename.startswith("error"):
        print(f"✅ Successfully generated: {video_filename}")
    else:
        print("❌ Video generation failed")
    
    # Open preview in browser
    webbrowser.open('file://' + os.path.abspath("reel_preview.html"))
    
    print("\n📋 Video Prompt:")
    print(f"{video_prompt[:300]}...")

if __name__ == "__main__":
    main()
