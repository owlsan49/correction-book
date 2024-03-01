<script setup lang="ts">
import { reactive, ref } from 'vue'
import { PushWords } from '@/apis/read.js'

// do not use same name with ref
const form = reactive({
    desc: '',
})

const onSubmit = () => {
    console.log('submit!')

    PushWords(form)
        .then(response => {
            console.log('success')
        }).catch(error => {
            console.log('error')
        })
}
</script>

<template>
    <el-form :model="form" label-width="120px">
        <el-form-item label="Words">
            <el-input v-model="form.desc" type="textarea" />
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="onSubmit">Submit</el-button>
        </el-form-item>
    </el-form>
</template>

<style>
.el-textarea__inner {
  height: 600px;
}

body {
  margin-left: 80px; 
  margin-right: 80px;
}

</style>