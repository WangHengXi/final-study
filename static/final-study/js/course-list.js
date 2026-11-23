(() => {
  const list = document.querySelector("[data-course-list]");

  if (!list) {
    return;
  }

  const endpoint = list.dataset.courseDataUrl;
  const searchForm = document.querySelector("#course-search-form");
  const searchInput = document.querySelector("#q");
  const count = document.querySelector("#course-count");
  const pagination = document.querySelector("#course-pagination");
  const status = document.querySelector("#course-list-status");
  const errorContainer = document.querySelector("#course-list-error");
  let activeRequest = 0;
  let abortController;
  let hasSuccessfulResult = false;

  const readLocation = () => {
    const parameters = new URLSearchParams(window.location.search);
    const rawPage = Number.parseInt(parameters.get("page") || "1", 10);

    return {
      query: parameters.get("q") || "",
      page: Number.isInteger(rawPage) && rawPage > 0 ? rawPage : 1,
    };
  };

  const replaceLocation = ({ query, page }, historyMode) => {
    const url = new URL(window.location.href);

    if (query) {
      url.searchParams.set("q", query);
    } else {
      url.searchParams.delete("q");
    }
    url.searchParams.set("page", String(page));

    window.history[historyMode]({}, "", url);
  };

  const setStatus = (message) => {
    status.textContent = message;
  };

  const makeElement = (tagName, className, text) => {
    const element = document.createElement(tagName);
    element.className = className;
    element.textContent = text;
    return element;
  };

  const setControlsLoading = (isLoading) => {
    searchForm.querySelector('button[type="submit"]').disabled = isLoading;
    for (const button of pagination.querySelectorAll("button")) {
      button.disabled = isLoading || button.dataset.pageUnavailable === "true";
    }
  };

  const clearError = () => {
    errorContainer.replaceChildren();
    errorContainer.hidden = true;
  };

  const createRetryButton = (requestedState) => {
    const button = makeElement("button", "course-list__button", "重試");
    button.type = "button";
    button.addEventListener("click", () => {
      loadCourses(requestedState);
    });
    return button;
  };

  const createErrorPanel = (error, requestedState) => {
    const panel = document.createElement("div");
    panel.className = "course-list__error";
    const authenticationRequired = error.status === 401;
    panel.append(
      makeElement(
        "p",
        "font-bold",
        authenticationRequired ? "登入狀態已失效。" : "目前無法載入課程。",
      ),
      makeElement(
        "p",
        "mt-2 text-sm text-[#6f6777]",
        authenticationRequired
          ? "請重新登入後再試。"
          : "請檢查網路連線後重試。",
      ),
    );
    const actions = document.createElement("div");
    actions.className = "course-list__actions";
    actions.append(createRetryButton(requestedState));

    if (authenticationRequired) {
      const login = makeElement("a", "course-list__button", "重新登入");
      login.href = list.dataset.loginUrl;
      actions.append(login);
    }

    panel.append(actions);
    return panel;
  };

  const renderInitialLoading = () => {
    list.replaceChildren(
      makeElement("p", "course-list__state", "正在載入課程…"),
    );
  };

  const renderEmpty = (query) => {
    const state = document.createElement("div");
    state.className = "course-list__state";
    state.append(
      makeElement(
        "p",
        "font-bold",
        query ? "目前沒有符合條件的課程。" : "目前還沒有課程。",
      ),
      makeElement(
        "p",
        "mt-2 text-sm text-[#77717e]",
        query
          ? "試試其他關鍵字，或顯示全部課程。"
          : "從第一門課開始，建立自己的學習紀錄。",
      ),
    );

    if (query) {
      const clearSearch = makeElement(
        "button",
        "course-list__button mt-4",
        "顯示全部課程",
      );
      clearSearch.type = "button";
      clearSearch.addEventListener("click", () => {
        searchInput.value = "";
        loadCourses({ query: "", page: 1 }, "pushState");
      });
      state.append(clearSearch);
    }

    list.replaceChildren(state);
  };

  const renderCourses = (payload) => {
    list.replaceChildren();

    if (payload.items.length === 0) {
      return;
    }

    for (const course of payload.items) {
      const card = document.createElement("a");
      card.href = course.detail_url;
      card.className = "paper-card group block rounded-2xl p-5 transition hover:-translate-y-0.5 hover:border-[#c8b8d2] hover:shadow-md sm:p-6";

      const row = document.createElement("div");
      row.className = "flex items-center justify-between gap-4";
      const content = document.createElement("div");
      content.className = "min-w-0";
      content.append(
        makeElement("h2", "break-words text-xl font-bold group-hover:text-[#82748e]", course.name),
        makeElement("p", "mt-2 break-all font-mono text-sm font-semibold tracking-wider text-[#77717e]", course.code),
        makeElement("p", "mt-2 text-sm text-[#6f6777]", `建立者：${course.owner_display_name}`),
      );
      const arrow = makeElement(
        "span",
        "shrink-0 text-xl text-[#a49baa] transition group-hover:translate-x-1 group-hover:text-[#82748e]",
        "→",
      );
      arrow.setAttribute("aria-hidden", "true");
      row.append(content, arrow);
      card.append(row);
      list.append(card);
    }
  };

  const renderPagination = (payload, query) => {
    pagination.replaceChildren();

    if (payload.total_pages <= 1) {
      return;
    }

    const controls = document.createElement("div");
    controls.className = "flex flex-wrap items-center justify-center gap-3";
    const createPageButton = (label, page, disabled = false) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "course-pagination__button";
      button.textContent = label;
      button.disabled = disabled;
      button.dataset.pageUnavailable = String(disabled);

      if (!disabled) {
        button.addEventListener("click", () => {
          loadCourses({ query, page }, "pushState");
        });
      }

      return button;
    };

    controls.append(
      createPageButton("上一頁", payload.page - 1, payload.page <= 1),
      makeElement(
        "span",
        "text-sm font-semibold text-[#6f6777]",
        `第 ${payload.page} / ${payload.total_pages} 頁`,
      ),
      createPageButton(
        "下一頁",
        payload.page + 1,
        payload.page >= payload.total_pages,
      ),
    );
    pagination.append(controls);
  };

  const loadCourses = async (requestedState, historyMode = null) => {
    const requestId = ++activeRequest;
    abortController?.abort();
    abortController = new AbortController();
    clearError();
    list.setAttribute("aria-busy", "true");
    setControlsLoading(true);
    if (!hasSuccessfulResult) {
      renderInitialLoading();
      pagination.replaceChildren();
    }
    setStatus("正在載入課程。");

    const url = new URL(endpoint, window.location.origin);
    if (requestedState.query) {
      url.searchParams.set("q", requestedState.query);
    }
    url.searchParams.set("page", String(requestedState.page));

    try {
      const response = await fetch(url, {
        headers: { Accept: "application/json" },
        signal: abortController.signal,
      });

      if (!response.ok) {
        const error = new Error("course-data-request-failed");
        error.status = response.status;
        throw error;
      }

      const payload = await response.json();
      if (
        !Array.isArray(payload.items)
        || !Number.isInteger(payload.page)
        || !Number.isInteger(payload.total_count)
        || !Number.isInteger(payload.total_pages)
      ) {
        throw new Error("course-data-response-invalid");
      }

      if (requestId !== activeRequest) {
        return;
      }

      if (historyMode) {
        replaceLocation(
          { query: requestedState.query, page: payload.page },
          historyMode,
        );
      }
      if (payload.items.length === 0) {
        renderEmpty(requestedState.query);
      } else {
        renderCourses(payload);
      }
      renderPagination(payload, requestedState.query);
      hasSuccessfulResult = true;
      count.textContent = `${payload.total_count} 門課程`;
      list.setAttribute("aria-busy", "false");
      setControlsLoading(false);
      setStatus(`已載入第 ${payload.page} 頁，共 ${payload.total_count} 門課程。`);
    } catch (error) {
      if (error.name === "AbortError" || requestId !== activeRequest) {
        return;
      }

      list.setAttribute("aria-busy", "false");
      setControlsLoading(false);
      if (hasSuccessfulResult) {
        errorContainer.append(createErrorPanel(error, requestedState));
        errorContainer.hidden = false;
      } else {
        list.replaceChildren(createErrorPanel(error, requestedState));
        pagination.replaceChildren();
        count.textContent = "課程無法載入";
      }
      setStatus(
        error.status === 401
          ? "登入狀態已失效，請重新登入後再試。"
          : "課程載入失敗。請檢查網路連線後重試。",
      );
    }
  };

  searchForm.addEventListener("submit", (event) => {
    event.preventDefault();
    loadCourses(
      { query: searchInput.value.trim(), page: 1 },
      "pushState",
    );
  });

  window.addEventListener("popstate", () => {
    const state = readLocation();
    searchInput.value = state.query;
    loadCourses(state);
  });

  const initialState = readLocation();
  searchInput.value = initialState.query;
  loadCourses(initialState, "replaceState");
})();
