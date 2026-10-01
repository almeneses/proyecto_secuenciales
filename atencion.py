"""Atención real, recalculada sobre el prefijo de la traducción elegida."""
import base64

import torch


@torch.inference_mode()
def extraer_atencion(resultado, model):
    entrada = torch.tensor([resultado['entrada_ids']], device=model.device)
    mascara = torch.tensor([resultado['entrada_mascara']], device=model.device)
    salida = torch.tensor([resultado['salida_ids']], device=model.device)
    if salida.shape[1] < 2:
        raise ValueError('La salida no contiene ningún token generado.')
    # La consulta en posición t predice salida[t + 1], no salida[t].
    outputs = model(input_ids=entrada, attention_mask=mascara,
                    decoder_input_ids=salida[:, :-1], output_attentions=True,
                    use_cache=False, return_dict=True)
    if not outputs.cross_attentions or any(a is None for a in outputs.cross_attentions):
        raise ValueError('El modelo no devolvió cross-attention. Se requiere atención eager.')
    pesos = torch.stack([a[0].detach().float().cpu() for a in outputs.cross_attentions])
    if pesos.shape[2:] != (salida.shape[1] - 1, entrada.shape[1]):
        raise ValueError('La atención no coincide con los tokens de entrada y salida.')
    if not torch.isfinite(pesos).all() or (pesos < 0).any():
        raise ValueError('El modelo devolvió pesos de atención inválidos.')
    # Float32 evita inflar el iframe con millones de números escritos en JSON.
    return {'forma': list(pesos.shape),
            'pesos': base64.b64encode(pesos.numpy().astype('<f4', copy=False).tobytes()).decode('ascii')}
