function runCode() {
  const code = document.getElementById('codeArea').value;
  try {
    const result = eval(code); // BE CAREFUL: eval is risky for production!
    document.getElementById('output').textContent = result;
  } catch (error) {
    document.getElementById('output').textContent = error;
  }
}