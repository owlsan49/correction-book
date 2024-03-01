import service from "@/utils/request.js"

export function PushWords(updateData){
    return service.request({
        method: "post",
        url: "/push_words",
        data: updateData
    })
}