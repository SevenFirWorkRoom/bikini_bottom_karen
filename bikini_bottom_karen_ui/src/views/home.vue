<template>
    <div id="app">
        <div class="container">
            <canvas ref="canvas"></canvas>
        </div>
    </div>
</template>

<script>
import RecordRTC from 'recordrtc';

export default {
    data() {
        return {
            audioContext: null,
            analyser: null,
            audioBufferSource: null,
            canvas: null,
            canvasCtx: null,
            websocket: null,
            audioDataQueue: [], // 存储接收到的音频数据
            mediaStream: null, // 添加新的属性来存储媒体流
            /////////////////////

            recorder: null,
            audioBlob: null,
            isRecording: false,
            ////////////////////
        };
    },
    methods: {
        sendMessage(blob) {
            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
                this.ws.send(blob);
            } else {
                console.error('WebSocket is not connected');
            }
        },
        audioFileUpload(file) {
            if (!file) return;

            if (this.audioContext) {
                this.audioContext.close();
            }

            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            this.analyser.fftSize = 256;

            const fileReader = new FileReader();
            fileReader.onload = (e) => {
                this.audioContext.decodeAudioData(e.target.result).then((buffer) => {
                    this.audioBufferSource = this.audioContext.createBufferSource();
                    this.audioBufferSource.buffer = buffer;
                    this.audioBufferSource.connect(this.analyser);
                    this.analyser.connect(this.audioContext.destination);
                    this.audioBufferSource.start();
                    this.draw();
                });
            };
            fileReader.readAsArrayBuffer(file);
        },
        /**
         * 处理重连逻辑
         */
        handleReconnect() {
            console.log("[WebSocket] 正在重连")
            setTimeout(() => {
                this.startWebSocket(); // 重新连接
            }, 3000);
        },
        startWebSocket() {
            // 创建 WebSocket 连接
            this.ws = new WebSocket('ws://localhost:9700/ws');

            // 监听 WebSocket 打开事件
            this.ws.onopen = () => {
                console.log('[WebSocket] 建立连接');
            };

            // 监听 WebSocket 消息事件
            this.ws.onmessage = (event) => {
                if (event.data instanceof Blob) {
                    // 如果是 Blob 对象，自动播放文件
                    this.audioFileUpload(event.data);
                } else {
                    // 如果是普通消息
                    console.log('[WebSocket] 接受消息:', event.data);
                }
            };

            // 监听 WebSocket 关闭事件
            this.ws.onclose = () => {
                console.log('[WebSocket] 连接关闭');
                this.handleReconnect(); // 触发重连逻辑
            };

            // 监听 WebSocket 错误事件
            this.ws.onerror = (error) => {
                console.error('[WebSocket] 错误:', error);
            };
        },

        ////////////////////

        draw() {
            const canvas = this.$refs.canvas;
            this.canvasCtx = canvas.getContext("2d");
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;

            const bufferLength = this.analyser.frequencyBinCount;
            const dataArray = new Uint8Array(bufferLength);
            const drawVisualizer = () => {
                requestAnimationFrame(drawVisualizer);

                this.analyser.getByteFrequencyData(dataArray);

                // 清空画布
                this.canvasCtx.fillStyle = "black";
                this.canvasCtx.fillRect(0, 0, canvas.width, canvas.height);

                const centerX = canvas.width / 2;
                const centerY = canvas.height / 2;
                const barWidth = (canvas.width / bufferLength) * 2;
                let xLeft = centerX; // 左侧起点
                let xRight = centerX; // 右侧起点

                for (let i = 0; i < bufferLength; i++) {
                    const barHeight = dataArray[i] / 2;

                    // 左侧波形
                    this.canvasCtx.fillStyle = "white";
                    this.canvasCtx.fillRect(xLeft - barWidth, centerY - barHeight / 2, barWidth, barHeight);

                    // 右侧波形
                    this.canvasCtx.fillRect(xRight, centerY - barHeight / 2, barWidth, barHeight);

                    xLeft -= barWidth;
                    xRight += barWidth;
                }
            };

            drawVisualizer();
        },
        startRecording() {
            navigator.mediaDevices.getUserMedia({audio: true})
                .then((stream) => {
                    this.mediaStream = stream;
                    this.recorder = new RecordRTC(stream, {
                        type: 'audio',
                        mimeType: 'audio/webm',
                    });
                    
                    // 设置音频分析
                    if (!this.audioContext) {
                        this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
                    }
                    this.analyser = this.audioContext.createAnalyser();
                    this.analyser.fftSize = 256;
                    
                    const source = this.audioContext.createMediaStreamSource(stream);
                    source.connect(this.analyser);
                    
                    this.recorder.startRecording();
                    this.isRecording = true;
                    this.draw(); // 开始绘制可视化效果
                })
                .catch((error) => {
                    console.error('无法获取麦克风权限:', error);
                });
        },
        stopRecording() {
            if (this.recorder) {
                this.recorder.stopRecording(() => {
                    this.audioBlob = this.recorder.getBlob();
                    this.sendRecordingToBackend(this.audioBlob);
                    this.isRecording = false;
                    
                    // 清理音频相关资源
                    if (this.mediaStream) {
                        this.mediaStream.getTracks().forEach(track => track.stop());
                        this.mediaStream = null;
                    }
                });
            }
        },
        sendRecordingToBackend(blob) {
            this.sendMessage(blob)
            console.log("[WebSocket] 主动上传成功")
        },
        handleKeyDown(event) {
            if (event.code === 'Space' && !this.isRecording) {
                this.startRecording();
            }
        },
        handleKeyUp(event) {
            if (event.code === 'Space' && this.isRecording) {
                this.stopRecording();
            }
        },
        ////////////////////
    },
    async mounted() {
        // 启动 WebSocket 连接
        await this.startWebSocket();
        window.addEventListener('keydown', this.handleKeyDown);
        window.addEventListener('keyup', this.handleKeyUp);

    },
    beforeDestroy() {
        // 关闭 WebSocket 连接
        if (this.ws) {
            this.ws.close();
        }
        window.removeEventListener('keydown', this.handleKeyDown);
        window.removeEventListener('keyup', this.handleKeyUp);
    },
};
</script>

<style>
html,
body {
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: black;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    flex-direction: column;
}

canvas {
    display: block;
    position: absolute;
    top: 0;
    left: 0;
}

button, input {
    position: absolute;
    top: 10px;
    left: 10px;
    z-index: 10;
    color: white;
}
</style>
