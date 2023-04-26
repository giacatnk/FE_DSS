
export function lastWord(words) {
    var n = words.split(/[\s,]+/);
    return n[n.length - 1];
  }