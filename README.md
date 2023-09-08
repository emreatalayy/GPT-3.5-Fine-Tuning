# GPT-3.5-Fine-Tuning
## Fine Tuning Nedir?
Fine-tuning, derin öğrenme modellerinin genellikle büyük ve çeşitlilik arz eden bir veri kümesi üzerinde ilk olarak önceden eğitim görmesi ve ardından belirli bir görev ya da daha spesifik bir veri kümesi üzerinde ek eğitim almasını tanımlayan bir yaklaşımdır. Bu stratejik süreç, modelin önceden geniş bir veri seti üzerinde kazandığı genel bilgileri koruyarak aynı zamanda yeni ve daha spesifik verilere nasıl daha iyi tepki vereceğini öğrenmesini sağlar. Transfer öğrenme yaklaşımının bir parçası olan fine-tuning, genellikle büyük ölçekli modellerin maliyetini ve eğitim süresini azaltmak için tercih edilir; çünkü modelin baştan tamamen eğitilmesi yerine, sadece belirli katmanları veya bölümleri ince ayarla eğitilir. ChatGpt 3.5 Turbonun Fine Tuning erşimi 22 Ağustos 2023'de açılmıştır. GPT 4 'ün ise sonbaharda erişime açalacağı söylenmektedir.

### ChatGPT 3.5 Nasıl Fine Tuning Yapılır ?
 GPT-3.5-Turbo modeli ile ince ayar yaparsanız, model 4 bin kelimeye kadar işlem yapabilir.İnce ayarın bir diğer avantajı da, modelin anlaması için verdiğiniz komutları daha kısa hale getirebilmeniz. İlk testleri yapanlar, komutları yüzde 90'a kadar kısaltmış ve bu sayede hem hız kazanmış hem de maliyeti düşürmüş. İnce ayar, tek başına bile etkili olsa da, diğer yöntemlerle birleştirildiğinde daha da güçlü oluyor. Sonbaharda, GPT-3.5-Turbo-16k modeli için de ince ayar yapılabilecek.

  # Fine-tuning Adımları

1. **Veriyi hazırlamak **
```json
{
  "messages": \[
{ "role": "system", "content": "You are a data science assistant." },
{ "role": "user", "content": "'state/reported/127488/1277622/0/boostPres: 198000' I want you to analyze this data " },
{ "role": "assistant", "content": "'path': 'state/reported/127488/1277622/0/boostPres', 'value': 198000, 'evaluation': 'Boost pressure measurement is 198000. This value seems abnormally high; please check for potential issues.'" }
  \]
},
```

Veriler JSON formatında olmak zorundadır.Genel protokolü de yukarıdaki gibidir. Genel mantık role, soru ve ideal cevap şeklinde gidiyor. Eğitim yapabilmek için en az 10 tane prompt- request çiftine ihtiyacımız var. Genel olarak eğitimin iyi bir sonuç vermesi için 
50 - 100 arası veri girmeniz tavsiye edilmektedir. Burada örneği JSON biçiminde gösterdim ancak yüklememiz gereken format .JSONL'dir. JSONL formatını bilmiyorsanız [buraya](https://hackernoon.com/json-lines-format-76353b4e588d) tıklayarak öğrenebilrsiniz. 

2. **Dosyayı Yükeleme**

Hazırladığımız JSONL formatındaki dosyamızı Train edilmesi için yükleyeceğiz. Bunun için aşağıdaki Python kodunu kullanabilirsiniz.
```python
import requests
api_key = "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"# kendi api keyiniz
file_path = "C:\\Users\\atala\\OneDrive\\Masaüstü\\fineTuning\\send_data3.jsonl" #yüklenecek dosyanın yolu
# API endpoint
url = "https://api.openai.com/v1/files"
# HTTP header
headers = {
    "Authorization": f"Bearer {api_key}"
}
with open(file_path, "rb") as f:
    response = requests.post(
        url,
        headers=headers,
        files={"file": f},
        data={"purpose": "fine-tune"}
    )
print(response.json())
```
**Print kısmında çıkan dosya ID kopyalamayı unutmayın diğer adımda lazım olacak.**






3. **Fine - Tuning Gerçekleştirme**

Aşağıdaki Python kodu ile Fine tuning işleminizi gerçekleştirebilirisiniz.
```python
import requests
import json
api_key = "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" # apı anahtar
training_file_id = "file-InJXS4kZSmOoVD1UYiV8T2B7" # bir önceki adımda yüklediğiniz dosyanın id si
url = "https://api.openai.com/v1/fine_tuning/jobs"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
data = {
    "training_file": training_file_id,
    "model": "gpt-3.5-turbo-0613"  # burada ise hangi modele fine tuning yapılacağını belirtiyosunuz
}
response = requests.post(url, headers=headers, json=data)
print(response.json())

```
Bu kodu çalışırdıktan sonra :
```json

{"object": "fine_tuning.job", "id": "ftjob-olSoq52LFCsPUSAzGSk4jZUf", "model": "gpt-3.5-turbo-0613", "created_at": 1693470516, "finished_at": null, "fine_tuned_model": null, "organization_id": "org-7BCRi2qMMKWqtOUo6ZQyY0oL", "result_files": [], "status": "created", "validation_file": null, "training_file": "file-5G5MEQox4qOJDTGvgGrgpiR5", "hyperparameters": {"n_epochs": 4}, "trained_tokens": null}
]
```
gibi bir sonuç dönecek. Burada "status": "created" ise model eğitilmeye başlanmıştır. Eğitim yaklaşık 5 dakika sürüyor. Eğitim bittikten sonra ise mail adresinize eğitimin bittiğine dair mesaj geliyor.

4. Modeli kullanma

Modeli eğitip eğitimin bittiğine dair mail geldikten sonra Fine tuning modelimizi kullanabiliriz.

```python
import openai
from colorama import Fore, init
init(autoreset=True)
api_key = ("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")
openai.api_key = api_key
def chat_with_gpt(messages_input, temperature=0.7, frequency_penalty=0, presence_penalty=0):
    completion = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::7twKh8Po", # buradaki 7twKh8Po kısımı mailde iletilen, modelin ID'si
        temperature=temperature,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        messages=messages_input
    )
    chat_response = completion['choices'][0]['message']['content']
    messages_input.append({"role": "assistant", "content": chat_response})
    return chat_response
# Function to print text in color if it contains certain keywords
def print_colored(agent, text):
    agent_colors = {
        "User": Fore.GREEN,
        "ChatBot1": Fore.CYAN
    }
    print(f"{agent_colors.get(agent, Fore.RESET)}{agent}: {text}")
if __name__ == "__main__":
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
    ]
    with open("metin.txt", "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        conversation.append({"role": "user", "content": line})
        response = chat_with_gpt(conversation)
        print_colored("User", line)
        print_colored("ChatBot1", response)
```
Bu kodda metin.txt'yi okuyup prompt olarak API'ya gönderiyor. Dilerseniz promptu farklı bir biçimde verebilirsiniz.

## Fiyatlandırma

İnce ayar maliyetleri iki gruba ayrılır: ilk eğitim maliyeti ve kullanım maliyeti.

Eğitim: 0,008 ABD Doları / 1K Token
Kullanım girişi: 0,012 ABD Doları / 1K Token
Kullanım çıktısı: 0,016 ABD Doları / 1K Token
Örneğin, 3 epoch için eğitilmiş 100.000 token( yani 100.000* 3  = 300.000) bir eğitim dosyasına sahip bir gpt-3.5-turbo ince ayar işinin yaklaşık maliyeti 2,40 ABD dolarıdır.

Son güncelleme tarihi : 08.09.2023
