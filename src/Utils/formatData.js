
// Input: Size as Byte
// Output: Format String
export function formatSize(size) {
    size = parseFloat(size)
    const postFix = ['Byte', 'KB', 'MB', 'GB', 'TB']
    var pos = 0 
    while (size > 1) 
    {
        size = size / 1024
        pos++
    }
    return `${(size*1024).toFixed(2)} ${postFix[pos - 1]}`
}