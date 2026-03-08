from transformers import AutoProcessor, SeamlessM4Tv2Model
import sounddevice as sd

print("1. 모델을 불러오는 중입니다...")
processor = AutoProcessor.from_pretrained("facebook/seamless-m4t-v2-large")
model = SeamlessM4Tv2Model.from_pretrained("facebook/seamless-m4t-v2-large")

print("2. 텍스트를 처리하고 영어 음성을 생성합니다...")
text_to_translate = "안녕하세요, 드디어 메타 다국어 모델 세팅을 완료했습니다! 이 음성은 파일 저장 없이 바로 재생됩니다."

# 한국어(kor) 텍스트를 입력받아 영어(eng) 음성으로 변환
text_inputs = processor(text=text_to_translate, src_lang="kor", return_tensors="pt")
audio_array_from_text = model.generate(**text_inputs, tgt_lang="eng")[0].cpu().numpy().squeeze()

print("3. 스피커로 오디오를 바로 재생합니다! 🔊")
sample_rate = model.config.sampling_rate

# 사운드 디바이스를 통해 배열(Array) 데이터를 즉시 재생
sd.play(audio_array_from_text, sample_rate)

# 오디오 재생이 끝날 때까지 프로그램이 종료되지 않고 기다리게 함 (필수!)
sd.wait() 

print("재생이 완료되었습니다!")