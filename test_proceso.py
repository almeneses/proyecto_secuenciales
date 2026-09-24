"""Comprobación sin descargar modelos: ejecutar con Python del entorno del proyecto."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

import torch
from streamlit.testing.v1 import AppTest
from proceso_transformer import crear_diagrama


def test_proceso():
    app = Path(__file__).with_name("Garcia_Marko_Rosenstiehl_Henry_Meneses_Alejandro_Tarea_Implementacion.py")
    tokenizer = Mock(return_value={"input_ids": torch.tensor([[12, 0]])})
    tokenizer.batch_decode.return_value = ["Hello"]
    tokenizer.convert_ids_to_tokens.side_effect = lambda ids: [str(i) for i in ids]
    tokenizer.encode.return_value = [12, 34]
    tokenizer.all_special_ids = [65000, 0]
    model = Mock(config=SimpleNamespace(encoder_layers=6, decoder_layers=6, encoder_attention_heads=8, d_model=512))
    model.generate.return_value = torch.tensor([[65000, 34, 0]])
    with patch("transformers.AutoTokenizer.from_pretrained", return_value=tokenizer), patch(
        "transformers.AutoModelForSeq2SeqLM.from_pretrained", return_value=model
    ):
        at = AppTest.from_file(str(app)).run()
        assert not at.exception and not at.checkbox[0].value
        assert not at.get("iframe")
        at.checkbox[0].check().run()
        assert not at.get("iframe") and not model.generate.called
        at.text_area[0].input("Hola   mundo hoy").run()
        at.button[0].click().run()
        assert not at.exception and at.success[0].value == "Hello"
        assert len(at.get("iframe")) == 1
        result = at.session_state["ultima_traduccion"]
        assert result["entrada_ids"] == [12, 0] and result["salida_ids"] == [65000, 34, 0]
        assert result["muestra_texto"] == "Hola mundo"
        assert result["muestra_ids"] == [12, 34]
        tokenizer.encode.assert_called_once_with("Hola mundo", add_special_tokens=False)
        assert tokenizer.call_args.args[0] == "Hola   mundo hoy"
        at.checkbox[0].uncheck().run()
        assert at.success[0].value == "Hello" and not at.get("iframe")
        at.checkbox[0].check().run()
        assert len(at.get("iframe")) == 1 and model.generate.call_count == 1
        at.selectbox[0].select("Inglés → Español").run()
        assert not at.success and not at.get("iframe")
        at.button[0].click().run()
        at.text_area[0].input("Otro texto").run()
        assert not at.success and not at.get("iframe")
        html = crear_diagrama('</script><script>alert("x")</script>', result)
        assert html.count("</script>") == 1
        assert "\\u003c/script>" in html
        assert "__DATOS__" not in html
    print("OK: visibilidad, persistencia sin reinferencia, invalidación y escape HTML")


if __name__ == "__main__":
    test_proceso()
