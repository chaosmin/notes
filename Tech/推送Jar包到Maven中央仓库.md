---
tags:
  - tech
  - maven
  - java
---

## GPG 密钥

### 生成 gpg 密钥

```bash
gpg --gen-key
# 提示输入名字和邮箱名称输入**命名空间的名称**即可。输入后，再输入O，回车。
# 然后会弹出要输入密码，这里会弹出一个让你输入密钥并二次确认的窗口,记住你的密码，后面发布的时候会用。（密码是为了保护私钥用的）
```

示例输出：

```bash
gpg (GnuPG) 2.4.8; Copyright (C) 2025 g10 Code GmbH
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Note: Use "gpg --full-generate-key" for a full featured key generation dialog.

GnuPG needs to construct a user ID to identify your key.

Real name: io.github.chaosmin
Email address: chaosmin@hotmail.com
You selected this USER-ID:
    "io.github.chaosmin <chaosmin@hotmail.com>"

Change (N)ame, (E)mail, or (O)kay/(Q)uit? O
We need to generate a lot of random bytes. It is a good idea to perform
some other action (type on the keyboard, move the mouse, utilize the
disks) during the prime generation; this gives the random number
generator a better chance to gain enough entropy.
gpg: revocation certificate stored as '/c/Users/Lenovo/.gnupg/openpgp-revocs.d/2506D18E8E7FAA4FCEF44D93EA5B8CA9F56E0AE4.rev'
public and secret key created and signed.

pub   ed25519 2026-04-02 [SC] [expires: 2029-04-01]
      2506D18E8E7FAA4FCEF44D93EA5B8CA9F56E0AE4
uid                      io.github.chaosmin <chaosmin@hotmail.com>
sub   cv25519 2026-04-02 [E] [expires: 2029-04-01]
```

上面 `2506D18E8E7FAA4FCEF44D93EA5B8CA9F56E0AE4` 就是密钥 id

### 发布 gpg 密钥

```bash
gpg --keyserver keyserver.ubuntu.com --send-keys 2506D18E8E7FAA4FCEF44D93EA5B8CA9F56E0AE4
```

这里发布到 `keyserver.ubuntu.com` 服务器上，这样中央仓库也有你的密钥，所以它才能验证你的身份

### 验证 gpg 密钥

```bash
gpg --keyserver keyserver.ubuntu.com --recv-keys 2506D18E8E7FAA4FCEF44D93EA5B8CA9F56E0AE4
```

出现下面的内容则说明发布成功

```bash
gpg: key EA5B8CA9F56E0AE4: "io.github.chaosmin <chaosmin@hotmail.com>" not changed
gpg: Total number processed: 1
gpg:              unchanged: 1
```

### 导出 gpg 公/私钥

备注：忘记了公钥，也可以通过 `gpg --list-keys` 查看当前所有的公钥

```bash
# 导出公钥
gpg -a -o public-file.key --export 2506D18E8E7FAA4FCEF44D93EA5B8CA9F56E0AE4
```

> -a 为 --armor 的简写，表示密钥以ASCII的形式输出，默认以二进制的形式输出；
> -o 为 --output 的简写，指定写入的文件；

```bash
# 导出私钥 （需要输入之前设置的保护私钥密码）
gpg -a -o private-file.key --export-secret-keys 2506D18E8E7FAA4FCEF44D93EA5B8CA9F56E0AE4
```

## Maven 注册

访问 [Maven Central](https://central.sonatype.com/) 并使用 Github 账户登录
登录成功后在 [Maven Central: Publishing](https://central.sonatype.com/publishing/namespaces) 页面查看命名空间是否已自动创建，如 `io.github.chaosmin`
打开 [central.sonatype.com/usertoken](https://central.sonatype.com/usertoken) 创建用户 Token

> [!note] 凭据
> `username` / `password` 见 [[Password.mdenc]] → Personal / Maven Central / User Token

```xml
<server>
    <id>${server}</id>
    <username>${SONATYPE_TOKEN_USERNAME}</username>
    <password>${SONATYPE_TOKEN_PASSWORD}</password>
</server>
```

## 接入项目
