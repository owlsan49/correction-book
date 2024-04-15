<script setup lang="ts">
import { ref, computed, toRef, onBeforeUnmount, onMounted } from 'vue'
import { PopWords, PushAddWords } from '@/apis/read.js'
let audioSource = ref('https://sensearch.baidu.com/gettts?lan=uk&spd=3&source=alading&text=')
let words = ref([])
let aWords = ref([])
let wordLength = ref(0)
let info = ref("")
let barPercentage = ref(0.0)
let currentIndex = ref(0)
let currentString = ref("")
let currentAudio = ref("")
let audioRef = ref()
let input_box = ref("")
let label = ref(-1)
const gap = 3

function addIndex() {
    if (label.value == 2) {
        if (currentIndex.value + 1 == words.value.length) {
            PushAddWords({'add_words': aWords.value})
        }
        currentIndex.value = (currentIndex.value + 1) % words.value.length
    }
    label.value = (label.value + 1) % gap
}

function addWords() {
    aWords.value.push(currentString.value)
}

function getWords() {
    PopWords({})
        .then(response => {
            words.value = response.data.words
            info.value = response.data.info
            wordLength.value = words.value.length

            if (words.value.length > 0) {
                barPercentage = computed(() => { return ((currentIndex.value / words.value.length) * 100) })
                console.log('@', barPercentage.value)
                currentString = computed(() => { return words.value[currentIndex.value] })
                console.log('@', currentString.value)
                currentAudio = computed(() => { return (audioSource.value + currentString.value) })
                console.log('@', currentAudio.value)
            }
        })
        .catch(error => {
            console.log(error)
        })
}

function handleKeydown(event: any) {
    if (event.key === 'Enter') {
        console.log('press enter')
        addIndex()
        if (label.value != 0) {
            togglePlay()
        }
    }

    if (event.key === '2') {
        console.log('press 1')
        aWords.value.push(currentString.value)
    }
    if (event.key === '1') {
        console.log('press 2')
        togglePlay()
    }
}

function togglePlay() {
    audioRef.value.play()
}

onBeforeUnmount(() => {
    console.log('@BeforeUnmount')
    window.removeEventListener('keydown', handleKeydown);
});
onMounted(() => {
    console.log('@onMounted')
    window.addEventListener('keydown', handleKeydown);
})
</script>

<template>
    <el-form-item>
        <el-button type="primary" @click="getWords">Review</el-button>
    </el-form-item>
    <p v-if="info.length">{{ info }}</p>
    <p v-else>We have {{ wordLength }} words to review Today</p>
    <hr>

    <div>
        <div class="demo-progress">
            <el-progress :text-inside="true" :stroke-width="40" :percentage="parseFloat(barPercentage.toFixed(2))" />
        </div>
        <audio ref="audioRef" :src="currentAudio" @canplay="() => { togglePlay() }"></audio>
        <el-button @click="togglePlay" class="el-icon-play">play</el-button>
        <el-button type="success" @click="addWords">add</el-button>
        <p v-if="label == 1">{{ currentString }}</p>
        <el-input v-model="input_box" placeholder="Please input" />
        <p v-if="aWords.length">{{ aWords }}</p>
    </div>
</template>

<style scoped>
.element {
    margin: 10px;
}
</style>