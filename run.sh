txt_filepath="$1"
output_directory_path="output"

text=$(<$txt_filepath)
model="en/ljspeech/tacotron2-DCA"
vocoder="en/ljspeech/univnet"

model_name=${model##*/}
vocoder_name=${vocoder##*/}
sample_name=${txt_filepath##*/}

tts --text "${text}" \
--model_name "tts_models/${model}" \
--out_path "${output_directory_path}/${vocoder_name}_${model_name}_${sample_name}.wav" \
--vocoder_name "vocoder_models/${vocoder}" ;
# --use_cuda "true" \