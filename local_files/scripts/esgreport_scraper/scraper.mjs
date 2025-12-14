// jina.mjs
async function searchESGWithJina(company, year = 2024) {
  const query = `"${company}" ("sustainability report" OR "esg report") (${year} OR ${year-1}) filetype:pdf`;
  const jinaUrl = `https://r.jina.ai/https://www.google.com/search?q=${encodeURIComponent(query)}&hl=en`;

  console.log(`[INFO] 🌐 Fetching via r.jina.ai for "${company}"...`);

  try {
    const res = await fetch(jinaUrl, {
      headers: { 'User-Agent': 'Mozilla/5.0' }
    });

    if (!res.ok) {
      console.log(`[ERROR] ❌ Jina returned ${res.status}`);
      return null;
    }

    const text = await res.text();
    console.log(`[DEBUG] 📄 Response length: ${text.length} chars`);

    // استخراج لینک‌های PDF
    const pdfRegex = /https?:\/\/[^\s\]]+\.pdf/gi;
    const matches = text.match(pdfRegex) || [];
    const filtered = matches.filter(url =>
      url.includes('report') || url.includes('sustainab') || url.includes('esg')
    );

    console.log(`[INFO] ✅ Found ${filtered.length} PDF links`);

    // تست سریع اولی
    for (const url of filtered) {
      try {
        const head = await fetch(url, { method: 'HEAD' });
        const ct = head.headers.get('content-type') || '';
        if (head.ok && (ct.includes('pdf') || ct.includes('octet-stream'))) {
          console.log(`[SUCCESS] 🎯 Valid PDF: ${url}`);
          return url;
        }
      } catch {}
    }

    return filtered[0] || null;

  } catch (err) {
    console.error(`[ERROR] 🚨 ${err.message}`);
    return null;
  }
}

// تست
const tests = [
  { company: "Maersk", year: 2024 },
  { company: "ZIM", year: 2023 },
];

console.log("🚀 ESG Search via r.jina.ai (no proxy needed)");
console.log("=".repeat(60));

for (const t of tests) {
  const url = await searchESGWithJina(t.company, t.year);
  console.log(`${url ? '✅' : '❌'} ${t.company}: ${url || '—'}`);
}