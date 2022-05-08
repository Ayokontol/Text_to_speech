txt_filepath="/content/drive/MyDrive/tts/$1" # path to the txt with the text to pronounce
output_directory_path="/content/drive/MyDrive/tts/random_samples_generated" # path to the directory to save generated wav

text=$(<$txt_filepath)
# "en/ljspeech/tacotron2-DDC_ph" "en/ljspeech/glow-tts" "en/ljspeech/tacotron2-DCA" "en/ljspeech/tacotron2-DDC"
models=("en/ljspeech/tacotron2-DCA")
# "en/ljspeech/multiband-melgan" "en/ljspeech/univnet" "en/ljspeech/hifigan_v2"
vocoders=("en/ljspeech/univnet")
# can pick any from --tts list-models

for vocoder in ${vocoders[@]}; do
  for model in ${models[@]}; do
    model_name=${model##*/} # grabs everything after the last '/'
    vocoder_name=${vocoder##*/}
    sample_name=${txt_filepath##*/}
    tts --text "${text}" \
    --model_name "tts_models/${model}" \
    --out_path ${output_directory_path}/${vocoder_name}/${model_name}/${sample_name}.wav \
    --vocoder_name "vocoder_models/${vocoder}" ;
    # --use_cuda "true" \
    done
done

echo "Files have been created!"
