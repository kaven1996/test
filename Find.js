// 等待页面加载完成
document.addEventListener('DOMContentLoaded', function() {
  // 通过ID选择表格
  const table = document.getElementById('data_mini');

  // 检查表格是否存在
  if (!table) {
    console.log('表格未找到');
    return;
  }

  // 存储结果的数组
  const result = [];

  // 遍历表格的每一行，跳过表头（假设第一行是表头）
  for (let i = 1; i < table.rows.length; i++) {
    const row = table.rows[i];
    const cells = row.cells;

    // 假设第二列是2nd token ratio，第三列是model，第四列是precision
    const secondTokenRatio = parseFloat(cells[1].textContent);
    const model = cells[2].textContent;
    const precision = parseFloat(cells[3].textContent);

    // 检查2nd token ratio是否大于5%
    if (secondTokenRatio > 0.05) {
      // 如果满足条件，将model和precision添加到结果数组
      result.push({
        model: model,
        precision: precision
      });
    }
  }

  // 打印或以其他方式使用结果
  console.log(result);
});