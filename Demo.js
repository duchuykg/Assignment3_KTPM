const { Builder, By, Key, until } = require("selenium-webdriver");

async function autotest() {
  // Khởi tạo trình duyệt
  const driver = await new Builder().forBrowser("chrome").build();

  try {
    // Điều hướng đến trang cần kiểm thử
    await driver.get("https://sandbox.moodledemo.net/login/index.php");

    await driver.findElement(By.id("username")).sendKeys("student");

    // Nhập mật khẩu và nhấn Enter
    await driver.findElement(By.id("password")).sendKeys("sandbox", Key.RETURN);

    // Chờ đến khi trang sau khi đăng nhập được tải
    await driver.findElement(By.linkText("My courses")).click();

    const button = await driver.findElement(By.css('li[data-key="mycourses"]'));

    await button.click();
    
  } finally {
    // Đóng trình duyệt
    // await driver.quit();

  }
}

// Gọi hàm kiểm thử tự động
autotest();
