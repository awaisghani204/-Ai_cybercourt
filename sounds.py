# Sound Effects using Web Audio API
import streamlit.components.v1 as components

def play_sound(sound_type):
    """Play a sound effect using Web Audio API via JavaScript injection."""
    
    sounds = {
        "gavel": """
        (function(){try{
            const c=new(window.AudioContext||window.webkitAudioContext)();
            const b=c.createBuffer(1,c.sampleRate*0.35,c.sampleRate);
            const d=b.getChannelData(0);
            for(let i=0;i<b.length;i++){
                const t=i/c.sampleRate;
                const noise=Math.random()*2-1;
                const thump=Math.sin(2*Math.PI*80*t);
                const crack=Math.sin(2*Math.PI*1200*t)*Math.exp(-t*40);
                d[i]=(noise*0.2+thump*0.5+crack*0.3)*Math.exp(-t*12)*0.6;
            }
            const s=c.createBufferSource();s.buffer=b;
            s.connect(c.destination);s.start();
        }catch(e){}})();
        """,
        "notification": """
        (function(){try{
            const c=new(window.AudioContext||window.webkitAudioContext)();
            const o=c.createOscillator();const g=c.createGain();
            o.type='sine';
            o.frequency.setValueAtTime(880,c.currentTime);
            o.frequency.setValueAtTime(1100,c.currentTime+0.1);
            g.gain.setValueAtTime(0.15,c.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+0.25);
            o.connect(g);g.connect(c.destination);
            o.start();o.stop(c.currentTime+0.25);
        }catch(e){}})();
        """,
        "verdict": """
        (function(){try{
            const c=new(window.AudioContext||window.webkitAudioContext)();
            [220,277.18,329.63,440].forEach(function(f,i){
                const o=c.createOscillator();const g=c.createGain();
                o.type='sine';o.frequency.value=f;
                const st=c.currentTime+i*0.2;
                g.gain.setValueAtTime(0.12,st);
                g.gain.exponentialRampToValueAtTime(0.001,st+1.8);
                o.connect(g);g.connect(c.destination);
                o.start(st);o.stop(st+1.8);
            });
        }catch(e){}})();
        """,
        "vote": """
        (function(){try{
            const c=new(window.AudioContext||window.webkitAudioContext)();
            const o=c.createOscillator();const g=c.createGain();
            o.type='triangle';
            o.frequency.setValueAtTime(600,c.currentTime);
            o.frequency.linearRampToValueAtTime(900,c.currentTime+0.15);
            g.gain.setValueAtTime(0.2,c.currentTime);
            g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+0.35);
            o.connect(g);g.connect(c.destination);
            o.start();o.stop(c.currentTime+0.35);
        }catch(e){}})();
        """
    }
    
    if sound_type in sounds:
        components.html(
            f'<script>{sounds[sound_type]}</script>',
            height=0, width=0
        )


def speak_verdict(text):
    """Speak the judge's verdict aloud using the browser's SpeechSynthesis API."""
    import json
    safe_text = json.dumps(text)  # Escapes quotes and special chars for JS
    
    js_code = f"""
    (function() {{
        try {{
            if ('speechSynthesis' in window) {{
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const text = {safe_text};
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.rate = 0.85;
                utterance.pitch = 0.8;
                utterance.volume = 1.0;
                
                let spoken = false;
                
                // Try to pick a deep/authoritative voice
                function speak() {{
                    if (spoken) return;
                    spoken = true;
                    
                    const voices = window.speechSynthesis.getVoices();
                    if (voices.length > 0) {{
                        // Prefer a male English voice
                        const preferred = voices.find(v => 
                            v.lang.startsWith('en') && v.name.toLowerCase().includes('male')
                        ) || voices.find(v => 
                            v.lang.startsWith('en') && v.name.toLowerCase().includes('david')
                        ) || voices.find(v => 
                            v.lang.startsWith('en')
                        ) || voices[0];
                        utterance.voice = preferred;
                    }}
                    window.speechSynthesis.speak(utterance);
                }}
                
                // Voices may load async
                if (window.speechSynthesis.getVoices().length > 0) {{
                    speak();
                }} else {{
                    window.speechSynthesis.onvoiceschanged = speak;
                }}
            }}
        }} catch(e) {{}}
    }})();
    """
    
    components.html(f'<script>{js_code}</script>', height=0, width=0)
