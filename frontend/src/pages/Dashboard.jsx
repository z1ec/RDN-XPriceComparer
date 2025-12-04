import { useEffect, useState } from "react";
import api from "../api/client";
import ProductTable from "../components/ProductTable";

export default function Dashboard({ onLogout }) {
  const [data, setData] = useState(null);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const username = localStorage.getItem("username") || "";

  const loadData = async () => {
    try {
      const res = await api.get("/data");
      setData(res.data);
    } catch (err) {
      setMessage("Ошибка загрузки данных");
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSave = async (payload) => {
    try {
      setSaving(true);
      setMessage("");
      await api.post("/update_product", payload);
      setMessage("Изменения сохранены");
      setTimeout(() => setMessage(""), 2000);
      await loadData();
    } catch (err) {
      setMessage("Ошибка сохранения");
    } finally {
      setSaving(false);
    }
  };

  const updatedAt = data?.updated_at
    ? new Date(data.updated_at).toLocaleString()
    : "-";

  return (
    <div className="min-h-screen">
      <header className="bg-white shadow-sm">
        <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold">Таблица цен</h1>
            <p className="text-xs text-slate-500">
              Пользователь: <span className="font-medium">{username}</span>{" "}
              · Обновлено: {updatedAt}
            </p>
          </div>

          <div className="flex items-center gap-3">
            {saving && (
              <span className="text-xs text-slate-500">Сохраняем...</span>
            )}
            <button
              className="text-xs text-slate-500 border px-2 py-1 rounded-lg hover:bg-slate-50"
              onClick={loadData}
            >
              Обновить данные
            </button>
            <button
              className="text-xs text-red-500 border border-red-300 px-2 py-1 rounded-lg hover:bg-red-50"
              onClick={onLogout}
            >
              Выйти
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6 space-y-4">
        {message && (
          <div className="text-sm text-center text-slate-700 bg-slate-100 border border-slate-200 rounded-lg py-2">
            {message}
          </div>
        )}

        {!data ? (
          <p className="text-sm text-slate-500">Загрузка...</p>
        ) : (
          <ProductTable products={data.products} onSave={handleSave} />
        )}
      </main>
    </div>
  );
}
