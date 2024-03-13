import service from "@/utils/request.js"

export function PushWords(updateData){
    return service.request({
        method: "post",
        url: "/push_words",
        data: updateData
    })
}

export function PushAddWords(updateData){
    return service.request({
        method: "post",
        url: "/push_add_words",
        data: updateData
    })
}

export function PopWords(updateParams){
    return service.request({
        method: "get",
        url: "/pop_words",
        params: updateParams
    })
}