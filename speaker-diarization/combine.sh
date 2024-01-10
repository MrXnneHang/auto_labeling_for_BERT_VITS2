export PYTHONPATH="${PYTHONPATH}:/home/xnne/local/code/auto_labeling_for_BERT_VITS2"
echo input the wav name: 
read wav_name
speaker_model_id=damo/speech_campplus_sv_zh-cn_16k-common

python local/voice_activity_detection.py --wavs examples/$wav_name.wav --out_file tmp/json/$wav_name.json
python local/prepare_subseg_json.py --vad tmp/json/$wav_name.json --out_file tmp/json/${wav_name}_seg.json
torchrun --nproc_per_node=1 local/extract_diar_embeddings.py --model_id $speaker_model_id --conf conf/diar.yaml \
          --subseg_json tmp/json/${wav_name}_seg.json --embs_out tmp/pkl/ --gpu "0" --use_gpu
torchrun --nproc_per_node=1 local/cluster_and_postprocess.py --conf conf/diar.yaml --embs_dir tmp/pkl --rttm_dir tmp/rttm
python utils/cut_segment_with_RTTM.py --rttm tmp/rttm/$wav_name.rttm --audio examples/$wav_name.wav --video examples/$wav_name.mp4 --output tmp/cut/$wav_name/
