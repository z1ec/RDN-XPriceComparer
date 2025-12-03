import { useState } from "react";

function App() {
  const [price, setPrice] = useState(null);
  const [loading, setLoading] = useState(false);

  async function loadPrice() {
    setLoading(true);
    setPrice(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/price");
      const data = await response.json();
      setPrice(data.price || "Цена не найдена");
    } catch (error) {
      setPrice("Ошибка запроса");
      console.error(error);
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 p-6">
      <div className="bg-white shadow-xl rounded-xl p-8 w-full max-w-lg text-center">

        <h1 className="text-2xl font-bold mb-4">
          Получить цену товара
        </h1>

        <button
          onClick={loadPrice}
          className="bg-blue-600 text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Показать цену
        </button>

        <div className="mt-6 text-lg">
          {loading && <p>Загрузка...</p>}
          {price && !loading && (
            <p className="font-semibold mt-4">
              Цена: <span className="text-green-600">{price}</span>
            </p>
          )}
        </div>

      </div>
    </div>
  );
}

export default App;
