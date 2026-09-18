## 2024-06-11 - Accessible Custom File Uploads
**Learning:** Custom file upload areas styled as labels (like `.upload-box` and `.upload-zone`) that hide the actual file `<input>` lose default keyboard accessibility. Users cannot tab to them or trigger the file dialog using Enter/Space without additional implementation.
**Action:** Always ensure that custom file dropzones/labels have `tabindex="0"`, `role="button"`, a visible `:focus-visible` outline, and a Javascript `keydown` listener that triggers the inner/hidden file input's `.click()` method upon Enter or Space keys.
