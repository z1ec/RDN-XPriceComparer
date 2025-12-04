import { useMemo, useState } from "react";

export default function ProductTable({ products, onSave }) {
  const [edited, setEdited] = useState({});
  const [search, setSearch] = useState("");
  const [tagFilter, setTagFilter] = useState("");
  const [sortField, setSortField] = useState("name");
  const [sortDir, setSortDir] = useState("asc");

  const handleChange = (id, field, value) => {
    setEdited((prev) => ({
      ...prev,
      [id]: {
        name_user: prev[id]?.name_user ?? "",
        tagsText: prev[id]?.tagsText ?? "",
        comment: prev[id]?.comment ?? "",
        ...prev[id],
        [field]: value
      }
    }));
  };

  const handleSave = (p) => {
    const current = edited[p.id] || {};
    const tagsText =
      current.tagsText !== undefined
        ? current.tagsText
        : (p.tags || []).join(", ");

    const payload = {
      product_id: p.id,
      name_user:
        current.name_user !== undefined ? current.name_user : p.name_user,
      tags: tagsText
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean),
      comment:
        current.comment !== undefined ? current.comment : p.comment
    };

    onSave(payload);
  };

  const viewProducts = useMemo(() => {
    let list = [...products];

    if (search.trim()) {
      const q = search.toLowerCase();
      list = list.filter((p) => {
        const n1 = (p.name_original || "").toLowerCase();
        const n2 = (p.name_user || "").toLowerCase();
        return n1.includes(q) || n2.includes(q);
      });
    }

    if (tagFilter.trim()) {
      const t = tagFilter.toLowerCase();
      list = list.filter((p) =>
        (p.tags || []).some((tag) => tag.toLowerCase().includes(t))
      );
    }

    list.sort((a, b) => {
      let v1;
      let v2;

      if (sortField === "name") {
        v1 = (a.name_user || a.name_original || "").toLowerCase();
        v2 = (b.name_user || b.name_original || "").toLowerCase();
      } else if (sortField === "price") {
        v1 = a.price || 0;
        v2 = b.price || 0;
      } else if (sortField === "tags") {
        v1 = (a.tags || []).length;
        v2 = (b.tags || []).length;
      } else {
        v1 = 0;
        v2 = 0;
      }

      if (v1 < v2) return sortDir === "asc" ? -1 : 1;
      if (v1 > v2) return sortDir === "asc" ? 1 : -1;
      return 0;
    });

    return list;
  }, [products, search, tagFilter, sortField, sortDir]);

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div className="flex gap-2 flex-1">
          <div className="flex-1">
            <label className="block text-xs font-medium mb-1">
              Поиск по названию
            </label>
            <input
              type="text"
              className="w-full border rounded-lg px-2 py-1 text-sm"
              placeholder="Введите название..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <div className="flex-1">
            <label className="block text-xs font-medium mb-1">
              Фильтр по тегу
            </label>
            <input
              type="text"
              className="w-full border rounded-lg px-2 py-1 text-sm"
              placeholder="Например: printer"
              value={tagFilter}
              onChange={(e) => setTagFilter(e.target.value)}
            />
          </div>
        </div>

        <div className="flex gap-2">
          <div>
            <label className="block text-xs font-medium mb-1">
              Сортировка
            </label>
            <select
              className="border rounded-lg px-2 py-1 text-sm"
              value={sortField}
              onChange={(e) => setSortField(e.target.value)}
            >
              <option value="name">По названию</option>
              <option value="price">По цене</option>
              <option value="tags">По количеству тегов</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium mb-1">
              Направление
            </label>
            <select
              className="border rounded-lg px-2 py-1 text-sm"
              value={sortDir}
              onChange={(e) => setSortDir(e.target.value)}
            >
              <option value="asc">↑ Возрастание</option>
              <option value="desc">↓ Убывание</option>
            </select>
          </div>
        </div>
      </div>

      <div className="overflow-auto bg-white rounded-2xl shadow">
        <table className="min-w-full text-sm">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-3 py-2 text-left font-semibold">ID</th>
              <th className="px-3 py-2 text-left font-semibold">Магазин</th>
              <th className="px-3 py-2 text-left font-semibold">Оригинальное название</th>
              <th className="px-3 py-2 text-left font-semibold">Моё название</th>
              <th className="px-3 py-2 text-left font-semibold">Цена</th>
              <th className="px-3 py-2 text-left font-semibold">Теги</th>
              <th className="px-3 py-2 text-left font-semibold">Комментарий</th>
              <th className="px-3 py-2 text-left font-semibold"></th>
            </tr>
          </thead>

          <tbody>
            {viewProducts.map((p) => {
              const edit = edited[p.id] || {};
              const nameUserValue =
                edit.name_user !== undefined ? edit.name_user : p.name_user || "";

              const tagsTextValue =
                edit.tagsText !== undefined
                  ? edit.tagsText
                  : (p.tags || []).join(", ");

              const commentValue =
                edit.comment !== undefined ? edit.comment : p.comment || "";

              return (
                <tr key={p.id} className="border-t">
                  <td className="px-3 py-2 text-xs text-slate-500">{p.id}</td>

                  <td className="px-3 py-2 text-xs text-slate-600 whitespace-nowrap">
                    {p.store || "-"}
                  </td>

                  <td className="px-3 py-2">
                    <div className="text-sm font-medium">{p.name_original}</div>
                  </td>

                  <td className="px-3 py-2">
                    <input
                      className="w-full border rounded-lg px-2 py-1 text-xs"
                      value={nameUserValue}
                      placeholder="Моё название"
                      onChange={(e) =>
                        handleChange(p.id, "name_user", e.target.value)
                      }
                    />
                  </td>

                  <td className="px-3 py-2 whitespace-nowrap">{p.price}</td>

                  <td className="px-3 py-2">
                    <input
                      className="w-full border rounded-lg px-2 py-1 text-xs"
                      value={tagsTextValue}
                      placeholder="tag1, tag2"
                      onChange={(e) =>
                        handleChange(p.id, "tagsText", e.target.value)
                      }
                    />
                  </td>

                  <td className="px-3 py-2">
                    <textarea
                      className="w-full border rounded-lg px-2 py-1 text-xs"
                      rows={2}
                      value={commentValue}
                      placeholder="Комментарий"
                      onChange={(e) =>
                        handleChange(p.id, "comment", e.target.value)
                      }
                    />
                  </td>

                  <td className="px-3 py-2">
                    <button
                      className="bg-blue-600 text-white text-xs px-3 py-1 rounded-lg"
                      onClick={() => handleSave(p)}
                    >
                      Сохранить
                    </button>
                  </td>
                </tr>
              );
            })}

            {viewProducts.length === 0 && (
              <tr>
                <td
                  colSpan={8}
                  className="px-3 py-4 text-center text-sm text-slate-500"
                >
                  Нет данных
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
