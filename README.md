## 🛠️ Figma to Unify Component Conversion (Text-Input)
Convert Figma text input components into Unify-compatible `e_component.json` files using Python.

---

### What This Does

1. **Step 1 (`extract_text_inputs.py`)**  
   Parses a Figma API JSON export and extracts text input-related data such as:
   - Label text
   - Placeholder
   - Hint/supporting text
   - Size and position
   - Component ID / type

   Output: `text_inputs.json`

2. **Step 2 (`convert_to_unify.py`)**  
   Converts the extracted inputs into a Unify-compatible `e_component.json` file that can be directly used to render the components in a Unify runtime environment.

   Output: `e_component.json`

---

---

### How to Run

1. Run the `extract_text_inputs` script to extract input fields from the Figma JSON  
   (generates `text_inputs.json`): `python3 extract_text_inputs.py`

2. Next, run the `convert_to_unify` script to produce the final component JSON  
   (reads from `text_inputs.json`, outputs `e_component.json`): `python3 convert_to_unify.py`

Both scripts should be run in order. Make sure `figma_response.json` is available before starting.



<p align="center">

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Mahavir2112/Task1-Unify/main/Figma_image.png" height="300"/><br/>
      <strong>Figma</strong>
    </td>
    <td align="center">
      <h1>➡️</h1>
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/Mahavir2112/Task1-Unify/main/Unify_image.png" height="300"/><br/>
      <strong>Unify Website</strong>
    </td>
  </tr>
</table>

</p>




