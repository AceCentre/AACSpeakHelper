# How was this made

Blood, sweat and tears

We have

1. A pipe server that&#x20;
   1. Reads in a config dict
   2. Creates an object to the TTS Engine and holds it in memory to reduce coldstart time
   3. Speaks using sounddevice
2. Client - calling executable
   1. You can pass it a config and a string or no string and it will use the pasteboard text
   2. Calls the pipe service

\
There is a lot of magic to make this work though. This includes

* [TTS-Wrapper ](https://github.com/willwade/tts-wrapper)- a unified wrapper to a range of TTS engines. This is needed as we need a unified way of get\_voices and speak, speak\_streamed etc
* [Sherpa-Onnx](https://github.com/k2-fsa/sherpa-onnx) - a really nice tooling pipleine to deal with VITS models that run on the edge
* [MMS](https://ai.meta.com/blog/multilingual-model-speech-recognition/) and [Models readied for Sherpa-Onnx](https://huggingface.co/willwade/mms-tts-multilingual-models-onnx) - Massive help this work from Meta - and it was "fun" converting their models for Sherpa-Onnx. We made some things on the way like a nice JSON with details on the voices
* QT/QT Threading. We had "fun" with threads. Never again

### Credits

* Will Wade (original v1, refactoring v2 several times, dealing with encryption, build scripts and generally pulling my hair out)
* Acer Jay Costillo (QT work and refactoring)
* Gavin Henderson - for making the call on baking in creds. I hated that and several times threw the idea out.&#x20;

**Whats next?**

* SAPI Bridge. This is really what is needed. C++ developers - we need your help
